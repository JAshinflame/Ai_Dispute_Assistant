import pandas as pd
from .utils import parse_date, mask_pii

def load_disputes(path, parse_dates=None):
    df = pd.read_csv(path, dtype=str)
    # common columns expected: dispute_id, description, amount, currency, transaction_id, transaction_date, dispute_date, merchant_name, status
    # normalize columns
    df = df.rename(columns=lambda s: s.strip() if isinstance(s, str) else s)
    # parse numeric
    if 'amount' in df.columns:
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    # parse dates
    for c in ['transaction_date','dispute_date']:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors='coerce', utc=False)
    # mask PII in text fields
    for c in df.columns:
        if df[c].dtype == object:
            df[c] = df[c].astype(str).apply(mask_pii)
    return df

def load_transactions(path):
    df = pd.read_csv(path, dtype=str)
    if 'amount' in df.columns:
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    for c in ['transaction_date']:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors='coerce', utc=False)
    return df
