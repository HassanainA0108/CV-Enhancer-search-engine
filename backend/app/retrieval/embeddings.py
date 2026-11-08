from functools import lru_cache
from fastembed import TextEmbedding, SparseTextEmbedding
from app.config import get_settings


@lru_cache
def dense_model():
    return TextEmbedding(model_name=get_settings().dense_model)


@lru_cache
def sparse_model():
    return SparseTextEmbedding(model_name='Qdrant/bm25')


def embed_dense(texts: list[str]) -> list[list[float]]:
    return [v.tolist() for v in dense_model().embed(texts)]


def embed_sparse(texts: list[str]):
    return list(sparse_model().embed(texts))
