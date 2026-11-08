from uuid import uuid4
from hashlib import sha256
from sqlalchemy import select, delete
from app.db.session import session_scope
from app.db.models import Resume, Job, Match
from app.schemas.job import MatchRequest
from app.intelligence.jd_analyzer import analyze_jd
from app.retrieval.hybrid_search import hybrid_search, CHUNK_COLLECTION, PROFILE_COLLECTION
from app.scoring.keyword_engine import keyword_score
from app.scoring.semantic_engine import semantic_scores
from app.scoring.decision_engine import combine_scores


def match_resumes(request: MatchRequest):
    with session_scope() as db:
        resumes = db.execute(select(Resume)).scalars().all()
        if not resumes:
            raise ValueError('No indexed resumes. Add files to data/resumes and run ingestion first.')
        digest = sha256(request.job_description.encode()).hexdigest()
        job = db.execute(select(Job).where(Job.jd_hash == digest)).scalars().first()
        if not job:
            analysis = analyze_jd(request.job_description)
            job = Job(id=str(uuid4()),jd_hash=digest,description=request.job_description,requirements=analysis.model_dump())
            db.add(job)
            db.commit()
        else:
            from app.schemas.job import JDAnalysis
            analysis = JDAnalysis.model_validate(job.requirements)
        # Both collections return independent evidence; keyword engine still scores ALL resumes.
        chunk_results = hybrid_search(request.job_description,CHUNK_COLLECTION,limit=35)
        profile_results = hybrid_search(request.job_description,PROFILE_COLLECTION,limit=max(25,len(resumes)))
        scores,evidence = semantic_scores(request.job_description,chunk_results,[r.id for r in resumes])
        # profiles avoid losing relevant full-resume hits because chunk retrieval is top-k.
        from app.retrieval.reranker import rerank
        profile_ids = [p['payload'].get('resume_id') for p in profile_results]
        profile_texts = [p['payload'].get('text','')[:1200] for p in profile_results]
        profile_raw = rerank(request.job_description[:1600],profile_texts) if profile_texts else []
        import math
        for rid, raw in zip(profile_ids,profile_raw):
            if rid:
                normalized = 100/(1+math.exp(-max(-30,min(30,raw))))
                scores[rid] = round(0.65*scores.get(rid,0)+0.35*normalized,2) if evidence.get(rid) else round(normalized,2)
        results = []
        for resume in resumes:
            key = keyword_score(analysis,resume.text,resume.sections or {})
            semantic = scores.get(resume.id,0.0)
            result = {
                'resume_id':resume.id,'filename':resume.filename,
                'semantic_score':semantic,'keyword_score':key['score'],
                'combined_score':combine_scores(semantic,key['score'],request.semantic_weight),
                'eligibility':key['eligibility'],
                'keyword_details':key['details'],
                'evidence':evidence.get(resume.id,[])[:5],
            }
            results.append(result)
        # Distinguish not-evidenced mandatory criteria; don't silently certify candidates.
        results.sort(key=lambda r:(r['eligibility']=='supported',r['combined_score']),reverse=True)
        db.execute(delete(Match).where(Match.job_id == job.id))
        for item in results:
            db.add(Match(job_id=job.id,resume_id=item['resume_id'],semantic_score=item['semantic_score'],keyword_score=item['keyword_score'],combined_score=item['combined_score'],details=item))
        db.commit()
        return {'job_id':job.id,'analysis':analysis.model_dump(),'ranking':results[:request.top_k],'total_resumes':len(resumes), 'disclaimer':'Scores are internal relevance/keyword indicators, not actual employer ATS pass probabilities.'}
