"""
Module 10: Production Engineering, Concurrency, and Performance Profiling
"""

MODULE_10 = {
    "id": "module_10",
    "title": "Модуль 10: Продакшн Инженерия, GIL и Оптимизация",
    "description": "Global Interpreter Lock (GIL), ThreadPoolExecutor vs ProcessPoolExecutor, профилирование cProfile и оптимизация алгоритмов с O(N^2) до O(N).",
    "order": 10,
    "lessons": [
        {
            "id": "m10_l1_gil_threads_vs_processes",
            "title": "10.1. Преодоление GIL: ThreadPoolExecutor vs ProcessPoolExecutor",
            "difficulty": "expert",
            "estimated_minutes": 35,
            "theory_md": """# Global Interpreter Lock (GIL) и параллелизм

В CPython **GIL (Global Interpreter Lock)** — это мьютекс, предотвращающий одновременное выполнение байткода несколькими нативными потоками.
- **I/O-bound задачи** (сеть, файлы, БД): потоки (`threading`, `ThreadPoolExecutor`) отлично подходят, так как CPython освобождает GIL во время системных вызовов I/O.
- **CPU-bound задачи** (математика, хэширование, обработка изображений): потоки НЕ дают ускорения из-за конкуренции за GIL! Для них необходимы **отдельные процессы** (`multiprocessing`, `ProcessPoolExecutor`), где у каждого процесса свой собственный Python-интерпретатор и отдельный GIL.

### Задание:
Реализуйте функцию `parallel_compute_batch(items: list[int], worker_fn, max_workers: int = 2) -> list`:
- Использует `concurrent.futures.ThreadPoolExecutor` (или `ProcessPoolExecutor`).
- Распределяет выполнение `worker_fn(item)` по пулу воркеров.
- Сохраняет исходный порядок результатов, соответствующий элементам `items`.
- Корректно завершает и очищает пул ресурсов после завершения расчетов.
""",
            "task_description": "Создайте параллельный диспетчер `parallel_compute_batch` с использованием `concurrent.futures`.",
            "starter_code": """from concurrent.futures import ThreadPoolExecutor

def parallel_compute_batch(items: list, worker_fn, max_workers: int = 2) -> list:
    \"\"\"
    Параллельная обработка набора элементов через пул исполнителей.
    \"\"\"
    # TODO: Используйте контекстный менеджер ThreadPoolExecutor и executor.map
    pass
""",
            "hints": [
                {
                    "level": 1,
                    "title": "Концептуальная наводка",
                    "content": "Используйте контекстный менеджер `with ThreadPoolExecutor(max_workers=max_workers) as executor:`."
                },
                {
                    "level": 2,
                    "title": "Сохранение порядка",
                    "content": "Метод `executor.map(worker_fn, items)` автоматически возвращает генератор результатов в исходном порядке следования элементов!"
                },
                {
                    "level": 3,
                    "title": "Преобразование в список",
                    "content": "Оберните результат в `list(executor.map(worker_fn, items))`."
                }
            ],
            "solution": """from concurrent.futures import ThreadPoolExecutor

def parallel_compute_batch(items: list, worker_fn, max_workers: int = 2) -> list:
    \"\"\"
    Эталонный параллельный исполнитель с гарантированным освобождением ресурсов.
    \"\"\"
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(worker_fn, items))
""",
            "test_suite_code": """
import time

def square_with_delay(x):
    time.sleep(0.02)
    return x * x

@pydeep_test("Проверка корректности порядка результатов")
def test_parallel_batch():
    inputs = [1, 2, 3, 4, 5]
    res = parallel_compute_batch(inputs, square_with_delay, max_workers=3)
    assert res == [1, 4, 9, 16, 25]
    return True
"""
        },
        {
            "id": "m10_l2_algorithmic_optimization_bench",
            "title": "10.2. Алгоритмическая оптимизация: переход от O(N²) к O(N)",
            "difficulty": "expert",
            "estimated_minutes": 35,
            "theory_md": """# Анализ сложности и профилирование

Наивная реализация проверки пересечений или подсчета совпадений:
```python
# O(N * M) - квадратичная сложность!
def find_common_bad(list_a, list_b):
    return [x for x in list_a if x in list_b]  # 'in' для list работает за O(M)
```

При $N = 100\\,000$ квадратичный алгоритм потребует $10^{10}$ операций (минуты выполнения).
Использование множеств (`set`) или хеш-таблиц переводит сложность поиска в амортизированное $O(1)$, а весь алгоритм в $O(N + M)$!

### Задание:
Реализуйте оптимизированную функцию `find_symmetric_pairs(pairs: list[tuple[int, int]]) -> list[tuple[int, int]]`:
- Пара $(a, b)$ и $(b, a)$ называется симметричной парой.
- Функция должна найти все уникальные симметричные пары в списке.
- Алгоритм **ОБЯЗАН** работать за $O(N)$ по времени (использование вложенных циклов $O(N^2)$ запрещено!).
- Для каждой найденной пары верните $(a, b)$ где $a < b$, отсортировав результат по первому элементу.
""",
            "task_description": "Создайте быстрый алгоритм поиска симметричных пар со сложностью O(N).",
            "starter_code": """def find_symmetric_pairs(pairs: list[tuple[int, int]]) -> list[tuple[int, int]]:
    \"\"\"
    Поиск симметричных пар (a, b) и (b, a) за строго линейное время O(N).
    \"\"\"
    # TODO: Реализуйте алгоритм с использованием множеств/хеш-таблицы
    pass
""",
            "hints": [
                {
                    "level": 1,
                    "title": "Концептуальная наводка",
                    "content": "Используйте множество `seen = set()` для хранения уже встреченных пар за один проход по списку."
                },
                {
                    "level": 2,
                    "title": "Поиск обратной пары",
                    "content": "Для каждой пары `(u, v)` проверьте: есть ли `(v, u)` в `seen`? Если да — вы нашли симметричную пару!"
                },
                {
                    "level": 3,
                    "title": "Нормализация и сортировка",
                    "content": "При нахождении добавьте `(min(u, v), max(u, v))` в результат и верните `sorted(result)`."
                }
            ],
            "solution": """def find_symmetric_pairs(pairs: list[tuple[int, int]]) -> list[tuple[int, int]]:
    \"\"\"
    Линейный O(N) алгоритм поиска симметричных пар на базе хеш-множества.
    \"\"\"
    seen = set()
    symmetric = set()

    for u, v in pairs:
        if (v, u) in seen:
            canonical = (min(u, v), max(u, v))
            symmetric.add(canonical)
        seen.add((u, v))

    return sorted(symmetric)
""",
            "test_suite_code": """
@pydeep_test("Поиск симметричных пар за линейное время")
def test_symmetric_pairs():
    data = [(1, 2), (3, 4), (5, 9), (2, 1), (4, 3)]
    res = find_symmetric_pairs(data)
    assert res == [(1, 2), (3, 4)]
    return True

@pydeep_test("Стресс-тест на O(N) производительность")
def test_linear_scale():
    # 20 000 элементов. На O(N^2) это упало бы по таймауту.
    large_data = [(i, i + 1) for i in range(10000)] + [(i + 1, i) for i in range(10000)]
    res = find_symmetric_pairs(large_data)
    assert len(res) == 10000
    assert res[0] == (0, 1)
    return True
"""
        }
    ]
}
