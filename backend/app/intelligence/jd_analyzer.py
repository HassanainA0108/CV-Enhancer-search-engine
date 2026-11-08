import re
from app.config import get_settings
from app.llm.azure_client import structured
from app.llm.prompts import JD_SYSTEM
from app.schemas.job import JDAnalysis, Requirement
from app.ingestion.resume_profiler import SKILL_TERMS


def analyze_jd(description: str) -> JDAnalysis:
    if get_settings().enable_llm:
        return structured(JD_SYSTEM, description[:22000], JDAnalysis)
    # Deterministic development fallback; not equivalent to full JD understanding.
    requirements = [Requirement(term=term, mandatory=True) for term in SKILL_TERMS if re.search(r'(?<!\w)' + re.escape(term) + r'(?!\w)', description, re.I)]
    role = next((line.strip()[:120] for line in description.splitlines() if line.strip()), 'Unspecified role')
    return JDAnalysis(role=role, requirements=requirements, notes=['LLM disabled: heuristic JD parsing used; verify requirement labels.'])
