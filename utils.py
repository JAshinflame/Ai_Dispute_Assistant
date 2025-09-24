import re
from datetime import datetime

def safe_lower(x):
    return str(x).lower() if x is not None else ''

def parse_date(x):
    if x is None or (isinstance(x, float) and str(x)=='nan'):
        return None
    if isinstance(x, datetime):
        return x
    for fmt in ('%Y-%m-%d','%Y/%m/%d','%d-%m-%Y','%m/%d/%Y','%Y-%m-%d %H:%M:%S'):
        try:
            return datetime.strptime(str(x), fmt)
        except Exception:
            pass
    # last resort
    try:
        return datetime.fromisoformat(str(x))
    except Exception:
        return None

def mask_pii(text):
    # Simple masking: replace 12-19 digit numbers (cards) and emails
    if text is None:
        return text
    s = str(text)
    s = re.sub(r'\b\d{12,19}\b', '[REDACTED_CARD]', s)
    s = re.sub(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', '[REDACTED_EMAIL]', s)
    return s
