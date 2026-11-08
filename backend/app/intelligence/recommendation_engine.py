from app.llm.azure_client import generate
from app.llm.prompts import EXPLANATION_SYSTEM


def recommend(jd: str, resume: str, match_details: dict):
    return generate(EXPLANATION_SYSTEM, f'''JOB DESCRIPTION:\n{jd[:14000]}\n\nRESUME:\n{resume[:20000]}\n\nMATCH ANALYSIS:\n{str(match_details)[:9000]}\n\nProvide: why this resume ranks well, missing or weak evidence, and a prioritized KEEP/REWRITE/REMOVE/ADD-ONLY-IF-TRUE plan. Include concrete proposed wording supported by the resume.''')
