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
        self.history = []
        self.func_info = []
        self.futures = []
        self.results = {}
        self.cpe = fut.ThreadPoolExecutor(max_workers=self.max_workers)

    def __del__(self):
        self.cpe.shutdown(wait=False)

    def concurrent_run(self, func: Callable) -> Callable:
        def wrapper(*args):
            signature = f'{func.__name__}{args}'
            if signature not in self.history:
                self.results[signature] = [self.cpe.submit(func, *args), None]
            self.history.append(signature)

        return wrapper

    def get_results(self) -> list[tuple[str, Any]]:
        for future in self.results.values():
            if err := future[0].exception():
                future[1] = repr(err)
            else:
                future[1] = future[0].result()
        return [(task_info, self.results[task_info][1]) for task_info in self.history]

"""
Done!
"""