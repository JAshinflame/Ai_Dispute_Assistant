try:
    from rapidfuzz import fuzz
    _HAS_RAPIDFUZZ = True
except Exception:
    _HAS_RAPIDFUZZ = False
    from difflib import SequenceMatcher

from datetime import datetime

def _merchant_similarity(a, b):
    if not a or not b:
        return 0.0
    if _HAS_RAPIDFUZZ:
        return fuzz.token_sort_ratio(a, b) / 100.0
    else:
        # fallback: simple ratio
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def compute_dup_score(merchant_a, merchant_b, amount_a, amount_b, date_a, date_b,
                      amount_tol_pct=0.02, date_window_days=2):
    try:
        merchant_sim = _merchant_similarity(merchant_a or '', merchant_b or '')
    except Exception:
        merchant_sim = 0.0
    # amount score
    try:
        abs_diff = abs((amount_a or 0) - (amount_b or 0))
        tol = max(amount_tol_pct * max(abs(amount_a or 0), abs(amount_b or 0)), 0.5)
        amount_score = 1.0 if abs_diff <= tol else max(0, 1 - (abs_diff / (max(abs(amount_a or 0), abs(amount_b or 0)) + 1e-6)))
    except Exception:
        amount_score = 0.0
    # date score
    try:
        if date_a is None or date_b is None:
            date_score = 0.0
        else:
            days_diff = abs((date_a - date_b).days)
            date_score = max(0, 1 - days_diff / date_window_days) if date_window_days>0 else 0
    except Exception:
        date_score = 0.0
    # weighted sum
    dup_score = 0.5 * merchant_sim + 0.3 * amount_score + 0.2 * date_score
    return float(dup_score)

def find_candidate_matches(dispute_row, transactions_df, top_k=5):
    # returns top_k transactions with highest dup_score
    scores = []
    for _, tx in transactions_df.iterrows():
        s = compute_dup_score(
            dispute_row.get('merchant_name',''),
            tx.get('merchant_name',''),
            float(dispute_row.get('amount') or 0),
            float(tx.get('amount') or 0),
            dispute_row.get('transaction_date'),
            tx.get('transaction_date')
        )
        scores.append((s, tx))
    scores.sort(key=lambda x: x[0], reverse=True)
    return scores[:top_k]
