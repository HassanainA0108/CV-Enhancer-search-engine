from app.llm.azure_client import generate
from app.llm.prompts import COVER_SYSTEM


def cover_letter(jd: str, resume: str, company: str):
    return generate(COVER_SYSTEM, f'Company: {company}\nJob description:\n{jd[:12000]}\n\nCandidate resume:\n{resume[:18000]}\n\nWrite a tailored cover letter (250-350 words).')
