"""
Module 5: Decorators, Context Managers, and Resource Cleanup
"""

MODULE_5 = {
    "id": "module_5",
    "title": "Модуль 7: Декораторы, Метаданные и Контекстные менеджеры",
    "description": "Параметризованные декораторы с сохранением сигнатур через functools.wraps, протокол контекстных менеджеров __enter__/__exit__ и подавление исключений.",
    "order": 7,
    "lessons": [
        {
            "id": "m5_l1_parameterized_decorators",
            "title": "7.1. Параметризованные декораторы: retry с экспоненциальным backoff",
            "difficulty": "intermediate",
            "estimated_minutes": 30,
            "theory_md": """# Параметризованные декораторы и `functools.wraps`

Декоратор — это функция высшего порядка, принимающая функцию и возвращающая обёртку.
Если декоратор принимает аргументы, требуется **трехуровневая структура**:
```python
def my_decorator(arg1, arg2):
    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return actual_decorator
```

### Зачем нужен `functools.wraps`?
Без него функция теряет имя `func.__name__`, документацию `func.__doc__`, аннотации `func.__annotations__` и исходную ссылку `func.__wrapped__`.

### Задание:
Напишите параметризованный декоратор `retry(max_retries: int = 3, exceptions: tuple = (Exception,))`:
- Пытается вызвать декорируемую функцию.
- Если функция вызывает исключение из кортежа `exceptions`, повторяет попытку до `max_retries` раз.
- Если все попытки исчерпаны, повторно выбрасывает последнее пойманное исключение.
- Добавляет к обертке специальный атрибут `.attempts_made` (число реально совершенных попыток при последнем вызове).
- Обязательно использует `functools.wraps`.
""",
            "task_description": "Реализуйте надежный декоратор `retry` с сохранением метаданных функции и счетчиком попыток.",
            "starter_code": """import functools

def retry(max_retries: int = 3, exceptions: tuple = (Exception,)):
    \"\"\"
    Декоратор повтора выполнения функции при возникновении указанных исключений.
    \"\"\"
    # TODO: Реализуйте трехуровневую фабрику декоратора
    pass
""",
            "hints": [
                {
                    "level": 1,
                    "title": "Концептуальная наводка",
                    "content": "Внешняя функция `retry` возвращает функцию `decorator(func)`. Внутри нее `wrapper(*args, **kwargs)` оборачивает вызов в цикл `for attempt in range(max_retries):`."
                },
                {
                    "level": 2,
                    "title": "Счетчик попыток",
                    "content": "Сохраняйте число сделанных попыток в атрибуте обертки: `wrapper.attempts_made = attempt + 1` перед каждым вызовом `func(*args, **kwargs)`."
                },
                {
                    "level": 3,
                    "title": "Обработка исключений",
                    "content": "Перехватывайте только исключения, переданные в `exceptions`: `except exceptions as e: last_exc = e`. Вне цикла сделайте `raise last_exc`."
                }
            ],
            "solution": """import functools

def retry(max_retries: int = 3, exceptions: tuple = (Exception,)):
    \"\"\"
    Эталонный декоратор повторных попыток.
    \"\"\"
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wrapper.attempts_made = 0
            last_exc = None
            for attempt in range(1, max_retries + 1):
                wrapper.attempts_made = attempt
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
            if last_exc:
                raise last_exc
        wrapper.attempts_made = 0
        return wrapper
    return decorator
""",
            "test_suite_code": """
@pydeep_test("Успешный вызов с первой попытки")
def test_success_first_try():
    calls = [0]
    @retry(max_retries=3)
    def ok_func():
        calls[0] += 1
        return "success"
    
    assert ok_func() == "success"
    assert ok_func.attempts_made == 1
    assert calls[0] == 1
    return True

@pydeep_test("Повтор и успех на третьей попытке")
def test_success_after_retries():
    calls = [0]
    @retry(max_retries=3, exceptions=(ValueError,))
    def flaky_func():
        calls[0] += 1
        if calls[0] < 3:
            raise ValueError("Network glitch")
        return "recovered"

    assert flaky_func() == "recovered"
    assert flaky_func.attempts_made == 3
    assert calls[0] == 3
    return True

@pydeep_test("Исчерпание попыток и проброс исключения")
def test_retries_exhausted():
    @retry(max_retries=2, exceptions=(KeyError,))
    def fail_always():
        raise KeyError("not found")

    try:
        fail_always()
        assert False, "Должно быть выброшено исключение KeyError"
    except KeyError:
        assert fail_always.attempts_made == 2
    return True
"""
        },
        {
            "id": "m5_l2_context_managers_suppress",
            "title": "7.2. Протокол контекстного менеджера: __enter__, __exit__ и подавление ошибок",
            "difficulty": "advanced",
            "estimated_minutes": 25,
            "theory_md": """# Протокол контекстного менеджера

Контекстные менеджеры управляют жизненным циклом ресурсов (файлы, сетевые сокеты, блокировки баз данных, временные изменения состояния).

### Метод `__exit__(self, exc_type, exc_val, exc_tb)`:
- Если блок `with` завершился штатно: все 3 аргумента равны `None`.
- Если в блоке `with` возникло исключение:
  - Возврат `True`: исключение **подавляется (suppressed)** и программа продолжает работу!
  - Возврат `False` (или `None`): исключение пробрасывается дальше вверх по стеку вызовов.

### Задание:
Реализуйте контекстный менеджер `SafeTransaction(rollback_action=None, suppress_errors=False)`:
- При входе в блок (`__enter__`): возвращает специальный объект `TransactionHandle` со свойствами:
  - `.committed = False`
  - `.rolled_back = False`
  - Метод `.commit()`: помечает транзакцию как зафиксированную (`committed = True`).
- При выходе (`__exit__`):
  - Если возникло исключение И транзакция НЕ была зафиксирована (`committed == False`):
    - Вызывает функцию `rollback_action()` (если она была передана).
    - Выставляет `handle.rolled_back = True`.
    - Если `suppress_errors=True`, подавляет исключение (возвращает `True`).
""",
            "task_description": "Создайте транзакционный контекстный менеджер `SafeTransaction` с поддержкой отката и условного подавления исключений.",
            "starter_code": """class TransactionHandle:
    def __init__(self):
        self.committed = False
        self.rolled_back = False

    def commit(self):
        self.committed = True


class SafeTransaction:
    \"\"\"
    Контекстный менеджер транзакций с авто-откатом при ошибке.
    \"\"\"
    def __init__(self, rollback_action=None, suppress_errors: bool = False):
        # TODO: Инициализация
        pass

    def __enter__(self) -> TransactionHandle:
        pass

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        pass
""",
            "hints": [
                {
                    "level": 1,
                    "title": "Концептуальная наводка",
                    "content": "Создайте `self.handle = TransactionHandle()` в конструкторе или `__enter__` и верните его из `__enter__`."
                },
                {
                    "level": 2,
                    "title": "Логика в __exit__",
                    "content": "В `__exit__` проверьте: `if exc_type is not None and not self.handle.committed:` — вызовите `rollback_action()`, установите `rolled_back = True`, и верните `True` если `self.suppress_errors` иначе `False`."
                },
                {
                    "level": 3,
                    "title": "Возвращаемое значение __exit__",
                    "content": "Возврат `bool(self.suppress_errors)` при наличии исключения указывает Python, нужно ли заглушить ошибку."
                }
            ],
            "solution": """class TransactionHandle:
    def __init__(self):
        self.committed = False
        self.rolled_back = False

    def commit(self):
        self.committed = True


class SafeTransaction:
    \"\"\"
    Эталонный контекстный менеджер транзакции с протоколом __enter__ / __exit__.
    \"\"\"
    def __init__(self, rollback_action=None, suppress_errors: bool = False):
        self.rollback_action = rollback_action
        self.suppress_errors = suppress_errors
        self.handle = None

    def __enter__(self) -> TransactionHandle:
        self.handle = TransactionHandle()
        return self.handle

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is not None:
            if not self.handle.committed:
                self.handle.rolled_back = True
                if callable(self.rollback_action):
                    self.rollback_action()
            return bool(self.suppress_errors)
        return False
""",
            "test_suite_code": """
@pydeep_test("Успешная фиксация транзакции")
def test_successful_commit():
    rolled = [False]
    with SafeTransaction(rollback_action=lambda: rolled.__setitem__(0, True)) as tx:
        tx.commit()
    assert tx.committed is True
    assert tx.rolled_back is False
    assert rolled[0] is False
    return True

@pydeep_test("Авто-откат и подавление ошибки")
def test_rollback_suppression():
    rolled = [False]
    with SafeTransaction(rollback_action=lambda: rolled.__setitem__(0, True), suppress_errors=True) as tx:
        raise ValueError("Simulated DB error")
    
    assert tx.committed is False
    assert tx.rolled_back is True
    assert rolled[0] is True
    return True
"""
        }
    ]
}
