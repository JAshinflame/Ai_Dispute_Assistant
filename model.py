from typing import List, Tuple
import logging
logger = logging.getLogger(__name__)

def predict_batch(rows):
    out = []
    for _ in rows:
        out.append(('OTHERS', 0.6, 'Fallback model prediction (no trained model)'))
    return out
