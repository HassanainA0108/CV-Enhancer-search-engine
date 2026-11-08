from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.db.models import Resume
from app.db.session import session_scope
router = APIRouter(prefix='/resumes',tags=['Resumes'])


@router.get('')
def list_resumes():
    with session_scope() as db:
        return [{'id':r.id,'filename':r.filename,'skills':(r.profile or {}).get('skills',[]),'updated_at':r.updated_at.isoformat() if r.updated_at else None} for r in db.execute(select(Resume)).scalars().all()]


@router.get('/{resume_id}')
def detail(resume_id: str):
    with session_scope() as db:
        r = db.get(Resume,resume_id)
        if not r:
            raise HTTPException(404,'Resume not found')
        return {'id':r.id,'filename':r.filename,'sections':r.sections,'profile':r.profile}
