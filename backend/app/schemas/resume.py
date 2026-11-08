from pydantic import BaseModel


class IngestionSummary(BaseModel):
    indexed: int
    skipped: int
    failed: list[str]
    removed: int = 0
