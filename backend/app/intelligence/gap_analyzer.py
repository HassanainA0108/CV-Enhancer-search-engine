def gap_summary(match: dict):
    found = [x for x in match['keyword_details'] if x['status'] in ('exact','alias')]
    missing = [x for x in match['keyword_details'] if x['status'] not in ('exact','alias')]
    return {'matched':found,'not_evidenced':missing}
