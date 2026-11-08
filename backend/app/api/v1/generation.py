from fastapi import APIRouter,HTTPException
from app.schemas.job import GeneratedRequest
from app.services.generation_service import generate_recommendations, generate_letter
router=APIRouter(prefix='/jobs',tags=['Generation'])


@router.post('/{job_id}/recommendations')
def recommendations(job_id: str, data: GeneratedRequest):
    try:
        return {'content':generate_recommendations(job_id,data.resume_id)}
    except ValueError as e:
        raise HTTPException(404,str(e)) from e


@router.post('/{job_id}/cover-letter')
def cover(job_id: str,data:GeneratedRequest):
    try:
        return {'content':generate_letter(job_id,data.resume_id,data.company)}
    except ValueError as e:
        raise HTTPException(404,str(e)) from e
