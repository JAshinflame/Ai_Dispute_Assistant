import time
import logging
from typing import Dict, List
logger = logging.getLogger(__name__)

class Timer:
    def __init__(self):
        self.records = []
    def __call__(self, name):
        return _TimerContext(self, name)
    def add(self, name, secs):
        self.records.append((name, secs))
    def report(self):
        logger.info('Benchmark report:')
        for name, secs in self.records:
            logger.info('  - %s: %.3fs', name, secs)

class _TimerContext:
    def __init__(self, timer: Timer, name: str):
        self.timer = timer
        self.name = name
    def __enter__(self):
        self.t0 = time.time()
    def __exit__(self, exc_type, exc, tb):
        secs = time.time() - self.t0
        self.timer.add(self.name, secs)
