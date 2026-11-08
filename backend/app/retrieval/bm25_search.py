from qdrant_client import models
from app.retrieval.hybrid_search import get_qdrant, SPARSE, CHUNK_COLLECTION
from app.retrieval.embeddings import embed_sparse


def search(query: str, limit=20):
    sparse = embed_sparse([query])[0]
    return get_qdrant().query_points(collection_name=CHUNK_COLLECTION, query=models.SparseVector(indices=sparse.indices.tolist(), values=sparse.values.tolist()), using=SPARSE, limit=limit).points
