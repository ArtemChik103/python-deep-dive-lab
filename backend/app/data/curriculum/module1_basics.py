"""
Module 1: Python Core & Memory Model
From foundational variables to memory references, mutability, and closures.
"""

MODULE_1 = {
    "id": "module_1",
    "title": "Модуль 1: Ядро Python и Модель Памяти",
    "description": "Погружение в ссылочную модель Python, изменяемость объектов, id(), области видимости LEGB и замыкания.",
    "order": 1,
    "lessons": [
        {
            "id": "m1_l1_references_mutability",
            "title": "1.1. Ссылочная модель: id, is vs ==, изменяемость",
            "difficulty": "beginner",
            "estimated_minutes": 15,
            "theory_md": """# Ссылочная модель Python: Объекты и Ссылки

В Python **всё является объектом**, а переменные — это лишь **имена (ярлыки)**, указывающие на объекты в куче (heap).

### Ключевые понятия:
1. `id(obj)` — возвращает уникальный целочисленный идентификатор объекта (в CPython это адрес объекта в оперативной памяти).
2. Оператор `is` проверяет идентичность: `a is b` эквивалентно `id(a) == id(b)`.
3. Оператор `==` проверяет равенство значений: вызывает метод `__eq__`.
4. **Неизменяемые типы (Immutable):** `int`, `float`, `str`, `tuple`, `frozenset`, `bytes`.
5. **Изменяемые типы (Mutable):** `list`, `dict`, `set`, `bytearray`.

### Ловушка изменяемых аргументов по умолчанию:
```python
# ОШИБКА: список создаётся один раз при определении функции!
def append_to(item, target=[]):
    target.append(item)
    return target

# ПРАВИЛЬНО:
def append_to(item, target=None):
    if target is None:
        target = []
    target.append(item)
    return target
```

### Задание:
Напишите функцию `safe_accumulator(item, bucket=None, copy_mode=False) -> list`:
- Если `bucket` не передан (`None`), функция должна использовать новый пустой список.
- Если `copy_mode=True`, функция не должна модифицировать переданный `bucket`, а вернуть новый список с добавленным `item`.
- Если `copy_mode=False` и `bucket` передан, функция добавляет `item` в существующий `bucket` (мутируя его) и возвращает его.
""",
            "task_description": "Реализуйте функцию `safe_accumulator(item, bucket=None, copy_mode=False) -> list` согласно правилам работы с изменяемыми аргументами и копированием.",
            "starter_code": """def safe_accumulator(item, bucket=None, copy_mode: bool = False) -> list:
    \"\"\"
    Безопасный аккумулятор элементов с защитой от разделяемого изменяемого состояния.
    \"\"\"
    # TODO: Реализуйте функцию
    pass
""",
            "hints": [
                {
                    "level": 1,
                    "title": "Концептуальная наводка",
                    "content": "Обратите внимание: если bucket равен None, мы создаем новый список в локальной области видимости. При copy_mode=True мы не имеем права изменять переданный список."
                },
                {
                    "level": 2,
                    "title": "Алгоритмическая подсказка",
                    "content": "При copy_mode=True создайте поверхностную копию списка (например, list(bucket) или bucket.copy()), добавьте в неё item и верните. Если copy_mode=False, мутируйте bucket через .append(item)."
                },
                {
                    "level": 3,
                    "title": "Точные сигнатуры и условия",
                    "content": "```python\nif bucket is None:\n    bucket = []\nif copy_mode:\n    new_bucket = list(bucket)\n    new_bucket.append(item)\n    return new_bucket\nelse:\n    bucket.append(item)\n    return bucket\n```"
                }
            ],
            "solution": """def safe_accumulator(item, bucket=None, copy_mode: bool = False) -> list:
    \"\"\"
    Эталонное решение задачи о ссылках и изменяемости.
    Временная сложность: O(1) при обычном добавлении (амортизированное O(1)), O(N) при copy_mode=True.
    Память: O(1) in-place или O(N) при создании копии.
    \"\"\"
    if bucket is None:
        return [item]
    
    if copy_mode:
        # Создаём изолированную копию, чтобы избежать сайд-эффектов
        cloned = list(bucket)
        cloned.append(item)
        return cloned
    
    bucket.append(item)
    return bucket
""",
            "test_suite_code": """
@pydeep_test("Дефолтный bucket создает независимые списки")
def test_default_isolation():
    res1 = safe_accumulator(1)
    res2 = safe_accumulator(2)
    assert res1 == [1], f"Expected [1], got {res1}"
    assert res2 == [2], f"Expected [2], got {res2}"
    assert res1 is not res2, "Списки не должны разделять память!"
    return True

@pydeep_test("Модификация существующего bucket при copy_mode=False")
def test_in_place_mutation():
    initial = [10, 20]
    res = safe_accumulator(30, bucket=initial, copy_mode=False)
    assert res is initial, "Должен вернуться тот же самый объект bucket"
    assert initial == [10, 20, 30], "Исходный список должен быть мутирован"
    return True

@pydeep_test("Изоляция при copy_mode=True")
def test_copy_mode():
    initial = [100, 200]
    res = safe_accumulator(300, bucket=initial, copy_mode=True)
    assert res == [100, 200, 300]
    assert initial == [100, 200], "Исходный список НЕ должен измениться при copy_mode=True"
    assert res is not initial, "Должен вернуться новый объект списка"
    return True
"""
        },
        {
            "id": "m1_l2_scopes_legb_closures",
            "title": "1.2. Области видимости LEGB, nonlocal и замыкания",
            "difficulty": "beginner",
            "estimated_minutes": 20,
            "theory_md": """# Области видимости (LEGB) и Замыкания (Closures)

При поиске переменной CPython строго следует правилу **LEGB**:
1. **L**ocal — внутри текущей функции
2. **E**nclosing — во внешней объемлющей функции (замыкание)
3. **G**lobal — на уровне текущего модуля (`globals()`)
4. **B**uiltin — во встроенном модуле `builtins`

### Ключевые слова:
- `global var_name`: указывает компилятору искать переменную в глобальной области видимости модуля.
- `nonlocal var_name`: указывает компилятору искать переменную в ближайшей объемлющей (Enclosing) функции, минуя Local, но не доходя до Global.

### Анатомия замыкания:
Замыкание (closure) возникает, когда вложенная функция ссылается на переменные из области видимости объемлющей функции, и эти переменные сохраняются в специальном объекте ячейки:
`fn.__closure__[0].cell_contents`.

### Задание:
Создайте фабрику счетчиков вызовов: `create_call_tracker(initial_limit: int = 5)`.
Она должна возвращать кортеж из двух функций `(tracker, reset)`:
1. `tracker(value: int) -> dict`:
   - Увеличивает внутренний счетчик вызовов.
   - Поддерживает скользящую сумму переданных `value`.
   - Если число вызовов превысило `initial_limit`, генерирует исключение `RuntimeError("Limit exceeded")`.
   - Возвращает словарь: `{"calls": count, "total_sum": running_sum, "remaining": limit - count}`.
2. `reset(new_limit: int = None) -> None`:
   - Сбрасывает счетчик вызовов в 0, скользящую сумму в 0, и обновляет лимит (если `new_limit` задан).
""",
            "task_description": "Реализуйте функцию-замыкание `create_call_tracker(initial_limit: int = 5)` с использованием ключевого слова `nonlocal`.",
            "starter_code": """def create_call_tracker(initial_limit: int = 5):
    \"\"\"
    Создает замыкание для отслеживания вызовов и суммы.
    Возвращает (tracker_fn, reset_fn).
    \"\"\"
    # TODO: Реализуйте замыкание с переменными limit, count, total_sum
    pass
""",
            "hints": [
                {
                    "level": 1,
                    "title": "Концептуальная наводка",
                    "content": "Внутри create_call_tracker объявите локальные переменные: count = 0, total_sum = 0, limit = initial_limit. Затем используйте nonlocal во вложенных функциях."
                },
                {
                    "level": 2,
                    "title": "Использование nonlocal",
                    "content": "Внутри функции tracker используйте: `nonlocal count, total_sum`. Внутри reset используйте: `nonlocal count, total_sum, limit`."
                },
                {
                    "level": 3,
                    "title": "Схема реализации",
                    "content": "```python\ndef create_call_tracker(initial_limit: int = 5):\n    count = 0\n    total = 0\n    limit = initial_limit\n    \n    def tracker(value: int):\n        nonlocal count, total\n        if count >= limit:\n            raise RuntimeError('Limit exceeded')\n        count += 1\n        total += value\n        return {'calls': count, 'total_sum': total, 'remaining': limit - count}\n    \n    def reset(new_limit: int = None):\n        nonlocal count, total, limit\n        count = 0\n        total = 0\n        if new_limit is not None:\n            limit = new_limit\n            \n    return tracker, reset\n```"
                }
            ],
            "solution": """def create_call_tracker(initial_limit: int = 5):
    \"\"\"
    Эталонная реализация замыкания на базе LEGB и nonlocal.
    Каждая инстанция сохраняет независимые cell-объекты в __closure__.
    \"\"\"
    count = 0
    total_sum = 0
    limit = initial_limit

    def tracker(value: int) -> dict:
        nonlocal count, total_sum
        if count >= limit:
            raise RuntimeError("Limit exceeded")
        count += 1
        total_sum += value
        return {
            "calls": count,
            "total_sum": total_sum,
            "remaining": limit - count
        }

    def reset(new_limit: int = None) -> None:
        nonlocal count, total_sum, limit
        count = 0
        total_sum = 0
        if new_limit is not None:
            limit = new_limit

    return tracker, reset
""",
            "test_suite_code": """
@pydeep_test("Проверка счета вызовов и суммы")
def test_tracker_basic():
    track, reset = create_call_tracker(initial_limit=3)
    r1 = track(10)
    assert r1 == {"calls": 1, "total_sum": 10, "remaining": 2}
    r2 = track(25)
    assert r2 == {"calls": 2, "total_sum": 35, "remaining": 1}
    r3 = track(5)
    assert r3 == {"calls": 3, "total_sum": 40, "remaining": 0}
    return True

@pydeep_test("Проверка исключения при превышении лимита")
def test_limit_exceeded():
    track, reset = create_call_tracker(initial_limit=1)
    track(100)
    try:
        track(200)
        assert False, "Должна быть ошибка RuntimeError при превышении лимита"
    except RuntimeError as e:
        assert "Limit exceeded" in str(e)
    return True

@pydeep_test("Проверка reset и обновления лимита")
def test_reset():
    track, reset = create_call_tracker(initial_limit=2)
    track(50)
    track(50)
    reset(new_limit=5)
    res = track(10)
    assert res == {"calls": 1, "total_sum": 10, "remaining": 4}
    return True
"""
        }
    ]
}
