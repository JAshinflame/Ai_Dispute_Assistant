def suggest_resolution(dispute_row, predicted_category, dup_score=None):
    # Basic mapping from category + signals -> suggested action
    amount = dispute_row.get('amount')
    tid = dispute_row.get('transaction_id') or dispute_row.get('transaction')
    if predicted_category == 'DUPLICATE_CHARGE':
        if dup_score is not None and dup_score >= 0.9 and (amount is None or float(amount) <= 1000):
            return 'Auto-refund', f'High duplicate score ({dup_score:.2f}) and original transaction appears settled; auto-refund recommended.'
        else:
            return 'Manual review - duplicate', f'Duplicate suspicion (dup_score={dup_score}); request agent review of receipts and transaction logs.'
    if predicted_category == 'FRAUD':
        return 'Escalate to bank / mark as fraud', 'Unauthorized claim; escalate to card issuer and block payment instrument pending investigation.'
    if predicted_category == 'REFUND_PENDING':
        return 'Escalate to payments / check refund flow', 'Refund appears to be pending; check processor logs and refund initiation timestamps.'
    if predicted_category == 'FAILED_TRANSACTION':
        return 'Inform customer / no refund', 'Transaction failed at gateway; no funds were captured. Explain failure and next steps to customer.'
    return 'Manual review', 'No automated resolution rule matched; route to agent for manual handling.'
