from pydantic import BaseModel, Field


class KeywordDetail(BaseModel):
    term: str
    mandatory: bool
    status: str
    matched_text: str | None = None
    section: str | None = None


class ScoreResult(BaseModel):
    resume_id: str
    filename: str
    semantic_score: float
    keyword_score: float
    combined_score: float
    eligibility: str
    keyword_details: list[KeywordDetail] = Field(default_factory=list)
    evidence: list[dict] = Field(default_factory=list)
