from typing import Tuple, Dict, Any
import logging
logger = logging.getLogger(__name__)

def suggest_resolution(dispute_row: Dict[str, Any], predicted_category: str, dup_score: float = 0.0) -> Tuple[str, str]:
    amount = dispute_row.get('amount')
    try:
        amt = float(amount) if amount not in (None, '') else None
    except Exception:
        amt = None
    if predicted_category == 'DUPLICATE_CHARGE':
        if dup_score >= 0.92 and (amt is None or amt <= 2000):
            return 'Auto-refund', f'Auto-refund recommended: dup_score={dup_score:.2f}; amount={amt}'
        return 'Manual review - duplicate', f'Duplicate suspected: dup_score={dup_score:.2f}; request agent verification.'
    if predicted_category == 'FRAUD':
        return 'Escalate to bank / mark as fraud', 'Unauthorized claim. Escalate to issuer and freeze instrument.'
    if predicted_category == 'REFUND_PENDING':
        return 'Escalate to payments team', 'Refund appears pending — check provider logs and ETA.'
    if predicted_category == 'FAILED_TRANSACTION':
        return 'Inform customer / close', 'Gateway failure; no capture occurred. Notify customer with guidance.'
    return 'Manual review', 'No clear automated action; send to agent queue.'
