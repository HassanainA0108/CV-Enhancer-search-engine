from fastapi import APIRouter,HTTPException
from app.schemas.job import MatchRequest
from app.services.matching_service import match_resumes
router=APIRouter(prefix='/jobs',tags=['Matching'])


@router.post('/match')
def match(data: MatchRequest):
    try:
        return match_resumes(data)
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e)) from e
