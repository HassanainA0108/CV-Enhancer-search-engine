from pydantic import BaseModel, Field


class Requirement(BaseModel):
    term: str
    mandatory: bool = True
    category: str = "skill"
    aliases: list[str] = Field(default_factory=list)


class JDAnalysis(BaseModel):
    role: str = "Unspecified role"
    requirements: list[Requirement] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)
    minimum_years: float | None = None
    notes: list[str] = Field(default_factory=list)


class MatchRequest(BaseModel):
    job_description: str = Field(min_length=30, max_length=50000)
    top_k: int = Field(default=5, ge=1, le=20)
    semantic_weight: float = Field(default=0.55, ge=0, le=1)


class GeneratedRequest(BaseModel):
    resume_id: str
    company: str = "the hiring organization"
