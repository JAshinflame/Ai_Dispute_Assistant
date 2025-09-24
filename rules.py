import re
from .utils import safe_lower

DUPLICATE_KEYWORDS = ['duplicate','double charge','charged twice','charged twice','charged twice to my account','charged twice.','double billed']
FRAUD_KEYWORDS = ['unauthorized','not me','stolen','fraud','card stolen','not authorized','unauthorised']
REFUND_PENDING_KEYWORDS = ['refund pending','refund not received','refund not processed','refund still pending']
FAILED_KEYWORDS = ['failed','declined','decline','insufficient','did not go through','not processed']

def match_keywords(text, keywords):
    if text is None:
        return False
    t = safe_lower(text)
    return any(k in t for k in keywords)

def rule_based_classify(row, dup_score=None):
    desc = row.get('description','') or ''
    # check duplicates based on description and dup_score
    if dup_score is not None and dup_score >= 0.9:
        return 'DUPLICATE_CHARGE', 0.95, f'Rule: high dup_score={dup_score:.2f}'
    if match_keywords(desc, DUPLICATE_KEYWORDS):
        return 'DUPLICATE_CHARGE', 0.92, 'Rule: description contains duplicate keywords'
    if match_keywords(desc, FRAUD_KEYWORDS):
        return 'FRAUD', 0.9, 'Rule: description indicates unauthorized/fraud'
    if match_keywords(desc, REFUND_PENDING_KEYWORDS) or ('refund' in safe_lower(desc) and 'pending' in safe_lower(desc)):
        return 'REFUND_PENDING', 0.9, 'Rule: refund pending keywords'
    if match_keywords(desc, FAILED_KEYWORDS):
        return 'FAILED_TRANSACTION', 0.88, 'Rule: gateway failure keywords'
    return None  # not matched
