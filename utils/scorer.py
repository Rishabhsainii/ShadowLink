# utils/scorer.py
def score_url_reason(url: str):
    url = url.lower()
    high = ['admin', 'login', 'backup', 'test', 'dev', 'debug', 'staging', 'secret']
    medium = ['api', 'private', 'config', 'internal']
    reason = "Generic resource"
    if any(k in url for k in high):
        reason = f"Contains high-risk keyword '{[k for k in high if k in url][0]}'"
        return "High", reason
    if any(k in url for k in medium):
        reason = f"Contains medium-risk keyword '{[k for k in medium if k in url][0]}'"
        return "Medium", reason
    return "Low", reason
