from app.retrieval.hybrid_search import get_qdrant, DENSE, CHUNK_COLLECTION
from app.retrieval.embeddings import embed_dense


def search(query: str, limit=20):
    return get_qdrant().query_points(collection_name=CHUNK_COLLECTION, query=embed_dense([query])[0], using=DENSE, limit=limit).points
