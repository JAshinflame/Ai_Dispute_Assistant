from typing import Tuple, List
import pandas as pd
import yaml
import os
import logging
from .logging_setup import setup_logging
from .data.loader import load_csv
from .rules import apply_rules_vectorized
from .duplicate.engine import batch_duplicate_detection
from .model import predict_batch
from .resolutions import suggest_resolution
import sqlite3
from time import time
from .benchmark import Timer

logger = logging.getLogger(__name__)

def load_config(path: str = None) -> dict:
    cfg_path = path or os.path.join(os.path.dirname(__file__), 'config.yaml')
    alt = os.path.join(os.getcwd(), 'ai_dispute_assistant_v2', 'config.yaml')
    if os.path.exists(alt):
        cfg_path = alt
    if os.path.exists(cfg_path):
        with open(cfg_path, 'r') as f:
            cfg = yaml.safe_load(f)
        return cfg
    return {}

def to_dict_rows(df: pd.DataFrame) -> List[dict]:
    return df.fillna('').to_dict(orient='records')

def write_sqlite(df: pd.DataFrame, path: str):
    conn = sqlite3.connect(path)
    df.to_sql('disputes', conn, if_exists='replace', index=False)
    conn.close()

def run_pipeline(disputes_path: str, transactions_path: str, out_dir: str = '/mnt/data') -> Tuple[pd.DataFrame, pd.DataFrame]:
    setup_logging()
    cfg = load_config()
    perf = cfg.get('performance', {})
    n_jobs = perf.get('n_jobs', -1)
    timer = Timer()

    with timer('load_data'):
        disputes = load_csv(disputes_path)
        transactions = load_csv(transactions_path)
    if 'merchant_name' not in disputes.columns:
        disputes['merchant_name'] = disputes.get('merchant', '')
    if 'merchant_name' not in transactions.columns:
        transactions['merchant_name'] = transactions.get('merchant', '')

    with timer('apply_rules'):
        rule_preds = apply_rules_vectorized(disputes) if cfg.get('pipeline', {}).get('rules', {}).get('enable', True) else pd.Series([None]*len(disputes), index=disputes.index)
        disputes['predicted_category'] = rule_preds
        disputes['explanation'] = disputes['predicted_category'].where(disputes['predicted_category'].notna(), other='')

    unresolved_mask = disputes['predicted_category'].isna()
    unresolved = disputes[unresolved_mask].copy()

    with timer('duplicate_detection'):
        disputes_rows = to_dict_rows(disputes)
        tx_rows = to_dict_rows(transactions)
        dup_cfg = cfg.get('pipeline', {}).get('duplicate', {})
        dup_cfg.setdefault('prune_threshold', 0.6)
        dup_cfg.setdefault('top_k', 3)
        dup_results = batch_duplicate_detection(disputes_rows, tx_rows, dup_cfg, n_jobs=n_jobs)
        dup_top_scores = [r[0][0] if r and len(r)>0 else 0.0 for r in dup_results]
        disputes['dup_top_score'] = dup_top_scores

    disputes.loc[disputes['predicted_category'].isna() & (disputes['dup_top_score'] >= dup_cfg.get('dup_score_threshold_auto', 0.92)), 'predicted_category'] = 'DUPLICATE_CHARGE'
    disputes.loc[disputes['predicted_category'].isna() & (disputes['dup_top_score'] > 0), 'explanation'] = disputes['explanation'] + 'dup_top_score=' + disputes['dup_top_score'].astype(str)

    remaining_mask = disputes['predicted_category'].isna()
    if remaining_mask.any() and cfg.get('pipeline', {}).get('model', {}).get('enable', False):
        rows = to_dict_rows(disputes[remaining_mask])
        preds = predict_batch(rows)
        for idx, (cat, conf, expl) in zip(disputes[remaining_mask].index, preds):
            disputes.at[idx, 'predicted_category'] = cat
            disputes.at[idx, 'explanation'] = expl

    disputes['predicted_category'] = disputes['predicted_category'].fillna('OTHERS')
    disputes['confidence'] = disputes.get('confidence', 0.6)

    with timer('suggest_resolutions'):
        actions = []
        justs = []
        for _, r in disputes.iterrows():
            action, just = suggest_resolution(r.to_dict(), r['predicted_category'], dup_score=float(r.get('dup_top_score') or 0.0))
            actions.append(action)
            justs.append(just)
        disputes['suggested_action'] = actions
        disputes['justification'] = justs

    out_classified = os.path.join(out_dir, 'classified_disputes_v2.csv')
    out_resolutions = os.path.join(out_dir, 'resolutions_v2.csv')
    disputes[['dispute_id','predicted_category','confidence','explanation','dup_top_score']].to_csv(out_classified, index=False)
    disputes[['dispute_id','suggested_action','justification']].to_csv(out_resolutions, index=False)

    if cfg.get('pipeline', {}).get('outputs', {}).get('sqlite', True):
        sqlite_path = os.path.join(out_dir, 'disputes_v2.sqlite')
        write_sqlite(disputes, sqlite_path)
        logger.info('Wrote sqlite DB: %s', sqlite_path)

    timer.report()
    return disputes, disputes[['dispute_id','suggested_action','justification']]
