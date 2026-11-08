from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.intelligence.jd_analyzer import analyze_jd
router=APIRouter(prefix='/jobs',tags=['Jobs'])


class AnalyzeRequest(BaseModel):
    job_description: str = Field(min_length=30)


@router.post('/analyze')
def analyze(data: AnalyzeRequest):
    return analyze_jd(data.job_description)
