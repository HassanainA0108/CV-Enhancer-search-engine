#Scores grounded JD-to-resume evidence; not Qdrant's raw RRF score."""
from collections import defaultdict
from app.retrieval.reranker import rerank


def semantic_scores(query: str, candidates: list[dict], all_resume_ids: list[str]) -> tuple[dict[str,float],dict[str,list[dict]]]:
    # Candidate chunk rows contain Qdrant payload, preserving resume_id.
    selected = candidates[:30]
    passages = [row['payload'].get('text','')[:1000] for row in selected]
    relevance = rerank(query[:1600], passages) if passages else []
    by_resume = defaultdict(list)
    for row, score in zip(selected, relevance):
        rid = row['payload'].get('resume_id')
        if rid:
            by_resume[rid].append({'section':row['payload'].get('section'), 'text':row['payload'].get('text','')[:450], 'reranker_raw':round(score,3)})
    # Reranker raw scores are model-dependent; apply a sigmoid and aggregate top evidence.
    import math
    scores = {}
    for rid in all_resume_ids:
        values = sorted([float(item['reranker_raw']) for item in by_resume[rid]], reverse=True)[:3]
        scores[rid] = round(100 * (sum(1/(1+math.exp(-max(-30,min(30,v)))) for v in values)/len(values)),2) if values else 0.0
    return scores, dict(by_resume)