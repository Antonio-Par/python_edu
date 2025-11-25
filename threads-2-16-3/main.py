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
        self.futures = []
        self.results = []
        self.cpe = fut.ThreadPoolExecutor(max_workers=self.max_workers)
        
    def concurrent_run(self, func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            self.func_info = f'{func.__name__}{args}'
            try:
                self.futures.append(self.cpe.submit(func, *args))
                done, _ = fut.wait(self.futures, timeout=1.5)
            finally:
                self.cpe.shutdown(wait=False, cancel_futures=False)
            for res in done:
                self.results.append((self.func_info, res.result()))
        return wrapper

    def get_results(self) -> list[tuple[str, Any]]:
        print(self.results)
        return self.results

executor = ConcurrentPoolExecutor(2)

@executor.concurrent_run
def task1(*args):
    return sum(args)


task1(1,2,3)
executor.get_results()

