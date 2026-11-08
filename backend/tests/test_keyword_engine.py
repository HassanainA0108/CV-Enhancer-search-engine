from app.scoring.keyword_engine import keyword_score, contains_term
from app.schemas.job import JDAnalysis, Requirement
from app.scoring.decision_engine import combine_scores


def test_exact_vs_not_equivalent():
    jd = JDAnalysis(requirements=[Requirement(term='AWS'), Requirement(term='CSPM'), Requirement(term='Terraform',mandatory=False)])
    result = keyword_score(jd,'Azure and cloud security posture management on Kubernetes',{'skills':'Azure and cloud security posture management on Kubernetes'})
    assert result['details'][0]['status'] == 'missing'
    assert result['details'][1]['status'] == 'alias'
    assert result['mandatory_not_evidenced'] == 1
    assert result['eligibility'] == 'needs_verification'


def test_terms_not_substrings():
    assert contains_term('FastAPI and Kubernetes', 'FastAPI')
    assert not contains_term('javascript', 'java')


def test_weighting():
    assert combine_scores(80,100,0.55) == 89


def test_empty_requirements_not_fake_perfect():
    result=keyword_score(JDAnalysis(), 'Python', {'skills':'Python'})
    assert result['score'] == 0
    assert result['eligibility'] == 'not_assessed'
