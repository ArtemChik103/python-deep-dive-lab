"""
Module 6: Asynchronous Programming with Asyncio
Coroutines, Tasks, Event Loop, asyncio.gather, TaskGroup, and Semaphore concurrency.
"""

MODULE_6 = {
    "id": "module_6",
    "title": "Модуль 8: Асинхронный Python (Asyncio)",
    "description": "Событийный цикл (Event Loop), корутины, конкурентный запуск задач, паттерны TaskGroup и регулирование нагрузки с asyncio.Semaphore.",
    "order": 8,
    "lessons": [
        {
            "id": "m6_l1_asyncio_concurrency_gather",
            "title": "8.1. Конкурентное выполнение корутин: asyncio.gather и TaskGroup",
            "difficulty": "advanced",
            "estimated_minutes": 30,
            "theory_md": """# Асинхронность и конкурентность в Python

В отличие от потоков ОС (threading), `asyncio` использует **кооперативную многозадачность** на базе одного потока и Event Loop:
1. Ключевое слово `async def` определяет корутину.
2. `await` приостанавливает выполнение корутины и передает управление обратно в Event Loop, пока выполняется неблокирующий I/O.
3. `asyncio.gather(*aws, return_exceptions=True)` запускает набор корутин параллельно во времени и собирает результаты.

### Задание:
Реализуйте асинхронную функцию `batch_fetch_simulator(task_ids: list[int], delays: list[float]) -> list[dict]`:
- Принимает список идентификаторов задач и список соответствующих задержек в секундах.
- Запускает асинхронную обработку каждой задачи параллельно с помощью `asyncio.sleep(delay)`.
- Для каждого `task_id` возвращает словарь:
  `{"id": task_id, "delay": delay, "status": "completed"}`.
- Задачи должны выполняться **одновременно**, так что суммарное время работы равно приблизительно $\\max(\\text{delays})$, а не сумме $\\sum \\text{delays}$!
""",
            "task_description": "Создайте асинхронную функцию `batch_fetch_simulator` для одновременного выполнения задач через `asyncio.gather`.",
            "starter_code": """import asyncio

async def batch_fetch_simulator(task_ids: list[int], delays: list[float]) -> list[dict]:
    \"\"\"
    Конкурентно выполняет обработку задач через asyncio.
    \"\"\"
    # TODO: Реализуйте корутину отдельной задачи и соберите через asyncio.gather
    pass
""",
            "hints": [
                {
                    "level": 1,
                    "title": "Концептуальная наводка",
                    "content": "Создайте вспомогательную внутреннюю функцию `async def process_item(task_id, delay): await asyncio.sleep(delay); return {...}`."
                },
                {
                    "level": 2,
                    "title": "Сборка задач через gather",
                    "content": "Создайте список корутин: `coros = [process_item(t_id, d) for t_id, d in zip(task_ids, delays)]` и вызовите `return await asyncio.gather(*coros)`."
                },
                {
                    "level": 3,
                    "title": "Полная реализация",
                    "content": "```python\nasync def batch_fetch_simulator(task_ids: list[int], delays: list[float]) -> list[dict]:\n    async def fetch(t_id, delay):\n        await asyncio.sleep(delay)\n        return {'id': t_id, 'delay': delay, 'status': 'completed'}\n    return await asyncio.gather(*(fetch(i, d) for i, d in zip(task_ids, delays)))\n```"
                }
            ],
            "solution": """import asyncio

async def batch_fetch_simulator(task_ids: list[int], delays: list[float]) -> list[dict]:
    \"\"\"
    Параллельная обработка I/O задач с использованием asyncio.gather.
    Время исполнения определяется максимальной, а не суммарной задержкой.
    \"\"\"
    async def worker(task_id: int, delay: float) -> dict:
        await asyncio.sleep(delay)
        return {
            "id": task_id,
            "delay": delay,
            "status": "completed"
        }

    tasks = [worker(tid, d) for tid, d in zip(task_ids, delays)]
    return list(await asyncio.gather(*tasks))
""",
            "test_suite_code": """
import asyncio
import time

@pydeep_test("Проверка параллельности выполнения")
def test_parallel_timing():
    # 3 задачи по 0.05 сек. Последовательно было бы 0.15s, параллельно ~0.05s
    start = time.perf_counter()
    res = asyncio.run(batch_fetch_simulator([1, 2, 3], [0.05, 0.05, 0.05]))
    duration = time.perf_counter() - start
    
    assert len(res) == 3
    assert res[0]["id"] == 1 and res[0]["status"] == "completed"
    assert duration < 0.12, f"Задачи должны выполняться конкурентно! Время: {duration:.2f}s"
    return True
"""
        },
        {
            "id": "m6_l2_async_semaphore_rate_limiter",
            "title": "8.2. Ограничение конкурентности: asyncio.Semaphore",
            "difficulty": "advanced",
            "estimated_minutes": 30,
            "theory_md": """# Ограничение параллелизма: `asyncio.Semaphore`

Когда вы запускаете тысячи сетевых запросов или соединений к базе данных, бесконтрольный запуск сотен задач одновременно приведет к исчерпанию файловых дескрипторов или блокировке IP со стороны сервиса.

`asyncio.Semaphore(max_concurrency)` гарантирует, что одновременно в критической секции находится не более заданного числа корутин:
```python
sem = asyncio.Semaphore(5)  # не более 5 одновременно

async def safe_worker():
    async with sem:
        # Критическая секция с сетевым запросом
        await download()
```

### Задание:
Реализуйте класс `AsyncRateLimiter(max_concurrent: int)`:
- Метод `async run_throttled(coros: list) -> list`:
  - Запускает список корутин.
  - Гарантирует, что в любой момент времени выполняется не более `max_concurrent` корутин.
  - Сохраняет максимальное число *одновременно активных* задач в свойстве `.peak_active`.
""",
            "task_description": "Создайте класс `AsyncRateLimiter` с использованием `asyncio.Semaphore` и трекингом пиковой нагрузки.",
            "starter_code": """import asyncio

class AsyncRateLimiter:
    \"\"\"
    Ограничитель параллельных корутин на базе семафора.
    \"\"\"
    def __init__(self, max_concurrent: int):
        self.max_concurrent = max_concurrent
        self.peak_active = 0
        # TODO: Инициализация семафора

    async def run_throttled(self, coroutine_factories: list) -> list:
        # TODO: Запустите фабрики корутин с ограничением семафора
        pass
""",
            "hints": [
                {
                    "level": 1,
                    "title": "Концептуальная наводка",
                    "content": "Используйте `self.semaphore = asyncio.Semaphore(self.max_concurrent)`. Для отслеживания пика создайте счетчик `active_count = 0`."
                },
                {
                    "level": 2,
                    "title": "Управление счетчиком активных задач",
                    "content": "Внутри блока `async with self.semaphore:` увеличивайте `active_count`, обновляйте `self.peak_active = max(self.peak_active, active_count)`, выполняйте `await coro_fn()`, и затем в `finally:` уменьшайте `active_count`."
                },
                {
                    "level": 3,
                    "title": "Сборка через gather",
                    "content": "```python\nasync def wrapped(fn):\n    async with self.semaphore:\n        active += 1\n        self.peak_active = max(self.peak_active, active)\n        try:\n            return await fn()\n        finally:\n            active -= 1\n```"
                }
            ],
            "solution": """import asyncio

class AsyncRateLimiter:
    \"\"\"
    Потокобезопасный ограничитель одновременных корутин.
    \"\"\"
    def __init__(self, max_concurrent: int):
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.peak_active = 0
        self._current_active = 0

    async def run_throttled(self, coroutine_factories: list) -> list:
        self.peak_active = 0
        self._current_active = 0

        async def worker(fn):
            async with self.semaphore:
                self._current_active += 1
                if self._current_active > self.peak_active:
                    self.peak_active = self._current_active
                try:
                    return await fn()
                finally:
                    self._current_active -= 1

        tasks = [worker(fn) for fn in coroutine_factories]
        return list(await asyncio.gather(*tasks))
""",
            "test_suite_code": """
import asyncio

@pydeep_test("Проверка соблюдения лимита семафора")
def test_semaphore_limit():
    limiter = AsyncRateLimiter(max_concurrent=2)

    async def dummy_job(val):
        await asyncio.sleep(0.04)
        return val * 2

    factories = [lambda v=i: dummy_job(v) for i in range(5)]
    results = asyncio.run(limiter.run_throttled(factories))

    assert results == [0, 2, 4, 6, 8]
    assert limiter.peak_active <= 2, f"Пиковое число задач не должно превышать 2! Было: {limiter.peak_active}"
    return True
"""
        }
    ]
}
