import pandas as pd
from .data_loader import load_disputes, load_transactions
from .duplicate_detection import find_candidate_matches, compute_dup_score
from .rules import rule_based_classify
from .resolutions import suggest_resolution
from .model import load_model, predict
import os

def run_pipeline(disputes_path, transactions_path, out_classified='/mnt/data/classified_disputes.csv', out_resolutions='/mnt/data/resolutions.csv', top_k=3):
    disputes = load_disputes(disputes_path)
    txns = load_transactions(transactions_path)

    results = []
    resolutions = []

    # index txns for quick access; ensure merchant_name column exists
    if 'merchant_name' not in txns.columns:
        txns['merchant_name'] = txns.get('merchant','')
    if 'merchant_name' not in disputes.columns:
        disputes['merchant_name'] = disputes.get('merchant','')

    model = load_model()

    for _, r in disputes.iterrows():
        row = r.to_dict()
        # find duplicate candidates
        candidates = find_candidate_matches(row, txns, top_k=top_k)
        top_score = candidates[0][0] if len(candidates)>0 else 0.0
        # apply rules
        rule = rule_based_classify(row, dup_score=top_score)
        if rule is not None:
            predicted, conf, explanation = rule
        else:
            # fallback to model if available
            if model is not None:
                pred_list = predict(model, pd.DataFrame([row]))
                predicted, conf, explanation = pred_list[0]
            else:
                predicted, conf, explanation = 'OTHERS', 0.6, 'Fallback default - no rule matched and no ML model available'
        results.append({
            'dispute_id': row.get('dispute_id') or row.get('id'),
            'predicted_category': predicted,
            'confidence': float(conf),
            'explanation': explanation,
            'dup_score_top': float(top_score)
        })
        action, justification = suggest_resolution(row, predicted, dup_score=top_score)
        resolutions.append({
            'dispute_id': row.get('dispute_id') or row.get('id'),
            'suggested_action': action,
            'justification': justification
        })

    df_out = pd.DataFrame(results)
    df_res = pd.DataFrame(resolutions)
    df_out.to_csv(out_classified, index=False)
    df_res.to_csv(out_resolutions, index=False)
    return df_out, df_res
