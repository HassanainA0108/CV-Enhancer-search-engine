'''Deterministic JD requirement coverage, independent of vector retrieval.'''

import re
from rapidfuzz.fuzz import ratio
from app.schemas.job import JDAnalysis, Requirement

ALIASES = {
    'cspm': ['cloud security posture management'],
    'iam': ['identity and access management'],
    'k8s': ['kubernetes'],
    'aks': ['azure kubernetes service'],
    'eks': ['elastic kubernetes service', 'amazon eks'],
    'rag': ['retrieval augmented generation', 'retrieval-augmented generation'],
    'llm': ['large language model'],
    'iac': ['infrastructure as code', 'infrastructure-as-code'],
    'ci/cd': ['continuous integration and continuous delivery', 'continuous integration and continuous deployment'],
    'aws': ['amazon web services'],
    'gcp': ['google cloud platform'],
}
CATEGORY_WEIGHTS = {'skill':1.0,'tool':1.0,'responsibility':0.8,'certification':1.3,'experience':1.2,'education':1.2}


def normalize(text: str):
    return re.sub(r'\s+', ' ', text.casefold().replace('–', '-').replace('—','-')).strip()


def contains_term(text: str, term: str):
    normalized = normalize(text)
    term = normalize(term)
    pattern = r'(?<![\w])' + re.escape(term) + r'(?![\w])'
    return bool(re.search(pattern, normalized))


def find_match(text: str, req: Requirement):
    possibilities = [req.term, *req.aliases, *ALIASES.get(req.term.casefold(), [])]
    for term in possibilities:
        if contains_term(text, term):
            return 'exact' if term.casefold() == req.term.casefold() else 'alias', term
    # Fuzzy typo detection is deliberately conservative. It is not full credit.
    for word in re.findall(r'[\w+.#/-]+', text):
        if len(req.term) >= 6 and abs(len(word)-len(req.term)) <= 1 and ratio(word.casefold(), req.term.casefold()) >= 94:
            return 'fuzzy', word
    return 'missing', None


def keyword_score(analysis: JDAnalysis, full_text: str, sections: dict[str,str]):
    evidence = []
    earned = possible = 0.0
    mandatory_count = 0
    mandatory_missing = 0
    for req in analysis.requirements:
        weight = (3.0 if req.mandatory else 1.0) * CATEGORY_WEIGHTS.get(req.category,1.0)
        possible += weight
        status, found = find_match(full_text, req)
        credit = {'exact':1.0,'alias':1.0,'fuzzy':0.35,'missing':0.0}[status]
        earned += weight * credit
        if req.mandatory:
            mandatory_count += 1
            if status == 'missing' or status == 'fuzzy':
                mandatory_missing += 1
        section = next((key for key,value in sections.items() if found and contains_term(value, found)),None)
        evidence.append({'term':req.term,'mandatory':req.mandatory,'status':status,'matched_text':found,'section':section})
    return {
        'score':round(100*earned/possible,2) if possible else 0.0,
        'details':evidence,
        'mandatory_total':mandatory_count,
        'mandatory_not_evidenced':mandatory_missing,
        'eligibility':'needs_verification' if mandatory_missing else ('supported' if mandatory_count else 'not_assessed'),
    }
