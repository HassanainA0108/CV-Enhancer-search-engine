from functools import lru_cache
from qdrant_client import QdrantClient, models
from app.config import get_settings
from app.retrieval.embeddings import embed_dense, embed_sparse

DENSE = 'dense'
SPARSE = 'bm25'
PROFILE_COLLECTION = 'resume_profiles'
CHUNK_COLLECTION = 'resume_chunks'


@lru_cache
def get_qdrant():
    s = get_settings()
    return QdrantClient(url=s.qdrant_url, api_key=s.qdrant_api_key or None, timeout=30)


def ensure_collections():
    client = get_qdrant()
    for collection in (PROFILE_COLLECTION, CHUNK_COLLECTION):
        if not client.collection_exists(collection):
            client.create_collection(
                collection_name=collection,
                vectors_config={DENSE: models.VectorParams(size=384, distance=models.Distance.COSINE)},
                sparse_vectors_config={SPARSE: models.SparseVectorParams(modifier=models.Modifier.IDF)},
            )
            client.create_payload_index(collection_name=collection, field_name='resume_id', field_schema=models.PayloadSchemaType.KEYWORD)


def upsert_documents(collection: str, records: list[dict]):
    if not records:
        return
    client = get_qdrant()
    dense = embed_dense([r['text'] for r in records])
    sparse = embed_sparse([r['text'] for r in records])
    points = []
    for record, dv, sv in zip(records, dense, sparse):
        payload = {k: v for k,v in record.items() if k != 'id'}
        points.append(models.PointStruct(
            id=record['id'],
            vector={DENSE: dv, SPARSE: models.SparseVector(indices=sv.indices.tolist(), values=sv.values.tolist())},
            payload=payload,
        ))
    client.upload_points(collection_name=collection, points=points, batch_size=32, wait=True)


def remove_resume(resume_id: str):
    selector = models.FilterSelector(filter=models.Filter(must=[models.FieldCondition(key='resume_id', match=models.MatchValue(value=resume_id))]))
    for name in (PROFILE_COLLECTION, CHUNK_COLLECTION):
        get_qdrant().delete(collection_name=name, points_selector=selector, wait=True)


def hybrid_search(query: str, collection: str = CHUNK_COLLECTION, limit: int = 25) -> list[dict]:
    dense = embed_dense([query])[0]
    sparse = embed_sparse([query])[0]
    points = get_qdrant().query_points(
        collection_name=collection,
        prefetch=[
            models.Prefetch(query=dense, using=DENSE, limit=max(limit, 30)),
            models.Prefetch(query=models.SparseVector(indices=sparse.indices.tolist(), values=sparse.values.tolist()), using=SPARSE, limit=max(limit, 30)),
        ],
        query=models.FusionQuery(fusion=models.Fusion.RRF),
        limit=limit,
        with_payload=True,
    ).points
    return [{'id':str(p.id),'rrf':float(p.score),'payload':p.payload or {}} for p in points]
