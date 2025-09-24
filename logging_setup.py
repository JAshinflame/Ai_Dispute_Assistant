import logging
from typing import Optional

def setup_logging(level: Optional[str] = 'INFO'):
    fmt = '%(asctime)s %(levelname)s [%(name)s] %(message)s'
    logging.basicConfig(level=getattr(logging, level.upper(), logging.INFO), format=fmt)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('botocore').setLevel(logging.WARNING)
