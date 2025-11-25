"""
Here we started doing the task
from 2.16 p.3
"""

import concurrent.futures as fut
from collections.abc import Callable
from typing import Any
import time


class ConcurrentPoolExecutor:
    def __init__(self, max_workers=1):
        self.max_workers = max_workers
        self.func_info = []
        self.results = None
        self.cpe = fut.ThreadPoolExecutor(max_workers=self.max_workers)
        
    def concurrent_run(self, func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            self.func_info = f'{func.__name__}{args}'
            self.cpe.submit(func, *args)
        return wrapper

    def get_results(self) -> list[tuple[str, Any]]:
        pass
