import re

SKILL_TERMS = ['Python','FastAPI','Django','Azure','AWS','GCP','Kubernetes','Docker','Terraform','IAM','RAG','LLMOps','MLOps','Machine Learning','AI Security','CSPM','NIST AI RMF','ISO 42001','SQL','OpenTelemetry','Pytorch','TensorFlow','GitHub Actions','CI/CD','Responsible AI']


def profile_resume(text: str, sections: dict[str,str]) -> dict:
    skills = [skill for skill in SKILL_TERMS if re.search(r'(?<!\w)' + re.escape(skill) + r'(?!\w)', text, re.I)]
    return {'skills':skills, 'sections':list(sections.keys()), 'summary':(sections.get('summary') or text)[:1500]}
