from typing import Tuple, Optional
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

RULE_KEYWORDS = {
    'DUPLICATE_CHARGE': ['duplicate','double charge','charged twice','double billed'],
    'FRAUD': ['unauthorized','not me','stolen','fraud','card stolen','not authorized','unauthorised'],
    'REFUND_PENDING': ['refund pending','refund not received','refund in transit','refund initiated'],
    'FAILED_TRANSACTION': ['failed','declined','decline','insufficient','did not go through','not processed']
}

def apply_rules_vectorized(df: pd.DataFrame) -> pd.Series:
    text_col = None
    for col in ['description','dispute_description','notes','comment']:
        if col in df.columns:
            text_col = col
            break
    if text_col is None:
        logger.debug('No text column found for rules; returning all None')
        return pd.Series([None]*len(df), index=df.index)
    s = df[text_col].fillna('').str.lower()
    out = pd.Series([None]*len(df), index=df.index)
    for cat, kws in RULE_KEYWORDS.items():
        mask = s.str.contains('|'.join([kw.replace(' ','\\s+') for kw in kws]), regex=True)
        out = out.where(~mask, other=cat)
    return out
