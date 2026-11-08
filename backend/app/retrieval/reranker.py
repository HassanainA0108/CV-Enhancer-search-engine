from functools import lru_cache
from fastembed.rerank.cross_encoder import TextCrossEncoder
from app.config import get_settings


@lru_cache
def get_reranker():
    return TextCrossEncoder(model_name=get_settings().reranker_model)


def rerank(query: str, passages: list[str]) -> list[float]:
    if not passages:
        return []
    return [float(value) for value in get_reranker().rerank(query, passages)]
