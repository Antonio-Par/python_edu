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
            if err := future.exception():
                self.results.append(repr(err))
            else:
                self.results.append(future.result())
        return list(zip(self.func_info, self.results))

# Работа тестирующей системы
print("\nТест №3")
executor = ConcurrentPoolExecutor(max_workers=3)

@executor.concurrent_run
def task1(*args):
    print(f"Вызвали task1 c аргументами {args}\n", end="", flush=True)
    time.sleep(0.2)
    return sum(args)

@executor.concurrent_run
def task2(*args):
    print(f"Вызвали task2 c аргументами {args}\n", end="", flush=True)
    time.sleep(0.2)
    raise ValueError("Пример ошибки")

# должны быть неблокирующие вызовы
start_time = time.perf_counter()
task1(1, 2, 3)
task1(1, 2, 3)
task1(1, 2, 3)
task1(4, 5)
task1(6, 7)
task1(8, 9)
task1(1, 2, 3)
task1(4, 5)
task2(1, 2, 3)
task1(10, 11)
task1(12, 13)
task1(14, 15)
task2(1, 2, 3)
task1(16, 17)
assert time.perf_counter()-start_time < 0.01, "Вызовы декорируемых функций должны быть неблокирующими!"

start_time = time.perf_counter()
for task_info, result in executor.get_results():
    print(f"{task_info} => {result}")
print(f"Вызов get_results занял {time.perf_counter()-start_time:.2f}")