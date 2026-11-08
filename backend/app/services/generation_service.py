from sqlalchemy import select
from app.db.models import Job,Resume,Match
from app.db.session import session_scope
from app.intelligence.recommendation_engine import recommend
from app.intelligence.cover_letter import cover_letter


def get_context(job_id: str,resume_id: str):
    with session_scope() as db:
        job = db.get(Job,job_id)
        resume = db.get(Resume,resume_id)
        match = db.execute(select(Match).where(Match.job_id==job_id,Match.resume_id==resume_id)).scalars().first()
        if not job or not resume or not match:
            raise ValueError('Job/resume match was not found')
        return job.description,resume.text,match.details


def generate_recommendations(job_id,resume_id):
    jd,resume,details = get_context(job_id,resume_id)
    return recommend(jd,resume,details)


def generate_letter(job_id,resume_id,company):
    jd,resume,_ = get_context(job_id,resume_id)
    return cover_letter(jd,resume,company)
