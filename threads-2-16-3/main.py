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

    def __del__(self):
        self.cpe.shutdown(wait=False)
        
    def concurrent_run(self, func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            self.func_info.append(f'{func.__name__}{args}')
            self.futures.append(self.cpe.submit(func, *args))
        return wrapper

    def get_results(self) -> list[tuple[str, Any]]:
        # done, _ = fut.wait(self.futures)
        # for res in done:
        for future in self.futures:
            self.results.append(future.result())

        print(list(zip(self.func_info, self.results)))
        return self.results


executor = ConcurrentPoolExecutor(2)


@executor.concurrent_run
def task1(*args):
    time.sleep(0.3)
    return sum(args)


@executor.concurrent_run
def task2(*args):
    time.sleep(0.1)
    return sum(args)


task1(1, 2, 3)
task2(1, 10, 3)
executor.get_results()

