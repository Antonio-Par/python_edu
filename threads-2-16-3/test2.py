# Работа тестирующей системы
print("\nТест №2")
executor = ConcurrentPoolExecutor(max_workers=2)

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
task1(4, 5)
task1(6, 7)
task1(8, 9)
task1(1, 2, 3)
task1(4, 5)
task2(1, 2, 3)
task1(10, 11)
task1(12, 13)
task2(1, 2, 3)
task1(14, 15)
assert time.perf_counter()-start_time < 0.01, "Вызовы декорируемых функций должны быть неблокирующими!"

start_time = time.perf_counter()
for task_info, result in executor.get_results():
    print(f"{task_info} => {result}")
print(f"Вызов get_results занял {time.perf_counter()-start_time:.2f}")