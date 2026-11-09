def combine_scores(semantic: float, keyword: float, semantic_weight: float = 0.55) -> float:
    return round(semantic*semantic_weight + keyword*(1-semantic_weight), 2)
