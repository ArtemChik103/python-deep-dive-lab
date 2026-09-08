"""
Module 2: Collections & Data Structures Internals
Hash tables, hash collisions, Big-O complexity, collections.deque and Counter.
"""

MODULE_2 = {
    "id": "module_2",
    "title": "Модуль 2: Коллекции и Внутреннее устройство Хеш-таблиц",
    "description": "Как устроен dict в CPython (compact dict), разрешение коллизий открытой адресацией, контракт __hash__ и __eq__, и структуры модуля collections.",
    "order": 2,
    "lessons": [
        {
            "id": "m2_l1_dict_internals_hash_contract",
            "title": "2.1. Контракт хеширования: __hash__, __eq__ и коллизии",
            "difficulty": "intermediate",
            "estimated_minutes": 25,
            "theory_md": """# Внутреннее устройство `dict` в CPython

С версии Python 3.6+ словари сохраняют порядок вставки благодаря **Compact Dict** архитектуре:
- Массив разреженных индексов `indices = [-1, 0, -1, 1, ...]`
- Плотный массив записей `entries = [(hash, key_ptr, value_ptr), ...]`

### Контракт хеширования в Python:
Для использования объекта в качестве ключа словаря или элемента `set`:
1. Объект должен быть **хешируемым (hashable)**.
2. Если `a == b`, то **ОБЯЗАТЕЛЬНО** `hash(a) == hash(b)`. (Обратное неверно: при одинаковом хеше объекты могут быть не равны — это **коллизия**).
3. Если переопределен `__eq__`, то Python автоматически сбрасывает `__hash__ = None`! Чтобы класс оставался хешируемым, нужно явно реализовать оба метода.
4. Хеш объекта не должен меняться на протяжении его жизни (объект должен быть иммутабельным по отношению к полям, используемым в хешировании).

### Задание:
Реализуйте класс `CaseInsensitiveKey`:
- Принимает строку `key: str`.
- Должен быть хешируемым и пригодным для использования в `dict` и `set`.
- Сравнение `==` должно быть регистронезависимым (`CaseInsensitiveKey("User") == CaseInsensitiveKey("user")` дает `True`).
- Метод `__hash__` должен гарантировать соответствие контракту (одинаковый хеш для ключей с разным регистром).
- Метод `__repr__` возвращает `CaseInsensitiveKey('original_value')`.
- Реализуйте свойство `.original` (возвращает исходную строку в исходном регистре).
""",
            "task_description": "Создайте класс `CaseInsensitiveKey` со строгим соблюдением контракта хеширования для использования в словарях.",
            "starter_code": """class CaseInsensitiveKey:
    \"\"\"
    Ключ словаря, игнорирующий регистр символов при сравнении и хешировании.
    \"\"\"
    def __init__(self, key: str):
        # TODO: Сохраните ключ и подготовьте нормализованное значение
        pass

    # TODO: Реализуйте __hash__, __eq__, __repr__ и свойство original
""",
            "hints": [
                {
                    "level": 1,
                    "title": "Концептуальная наводка",
                    "content": "Для регистронезависимого сравнения строк в Python рекомендуется метод .casefold() (он работает надежнее, чем .lower(), для всех языков)."
                },
                {
                    "level": 2,
                    "title": "Хеширование и сравнение",
                    "content": "Хешируйте именно результат self.key.casefold(). В __eq__ проверяйте, что другой объект тоже CaseInsensitiveKey (или str) и сравнивайте их casefold-значения."
                },
                {
                    "level": 3,
                    "title": "Готовый каркас",
                    "content": "```python\ndef __eq__(self, other):\n    if isinstance(other, CaseInsensitiveKey):\n        return self._normalized == other._normalized\n    if isinstance(other, str):\n        return self._normalized == other.casefold()\n    return False\n\ndef __hash__(self):\n    return hash(self._normalized)\n```"
                }
            ],
            "solution": """class CaseInsensitiveKey:
    \"\"\"
    Эталонная реализация иммутабельного регистронезависимого ключа.
    Полностью удовлетворяет PEP-3141 и контракту hash/eq.
    \"\"\"
    __slots__ = ('_original', '_normalized', '_hash')

    def __init__(self, key: str):
        if not isinstance(key, str):
            raise TypeError(f"Key must be a string, got {type(key).__name__}")
        self._original = key
        self._normalized = key.casefold()
        self._hash = hash(self._normalized)

    @property
    def original(self) -> str:
        return self._original

    def __hash__(self) -> int:
        return self._hash

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CaseInsensitiveKey):
            return self._normalized == other._normalized
        if isinstance(other, str):
            return self._normalized == other.casefold()
        return False

    def __repr__(self) -> str:
        return f"CaseInsensitiveKey({self._original!r})"
""",
            "test_suite_code": """
@pydeep_test("Проверка равенства при разном регистре")
def test_case_equality():
    k1 = CaseInsensitiveKey("Python")
    k2 = CaseInsensitiveKey("python")
    k3 = CaseInsensitiveKey("PYTHON")
    assert k1 == k2
    assert k2 == k3
    assert k1 == "python"
    return True

@pydeep_test("Проверка контракта __hash__ == __hash__")
def test_hash_contract():
    k1 = CaseInsensitiveKey("Header-Auth")
    k2 = CaseInsensitiveKey("header-auth")
    assert hash(k1) == hash(k2), "Хеши равных объектов ДОЛЖНЫ совпадать!"
    return True

@pydeep_test("Использование в качестве ключа dict")
def test_dict_usage():
    d = {}
    d[CaseInsensitiveKey("Authorization")] = "Bearer Token_123"
    assert d[CaseInsensitiveKey("authorization")] == "Bearer Token_123"
    assert d[CaseInsensitiveKey("AUTHORIZATION")] == "Bearer Token_123"
    assert len(d) == 1
    return True
"""
        },
        {
            "id": "m2_l2_sliding_window_deque",
            "title": "2.2. Сложность операций: deque vs list в скользящем окне",
            "difficulty": "intermediate",
            "estimated_minutes": 25,
            "theory_md": """# Временная сложность `list` vs `collections.deque`

В CPython `list` — это **динамический массив указателей** (`PyObject**`):
- Добавление в конец (`.append()`): амортизированное $O(1)$.
- Удаление/вставка в начало (`.pop(0)`, `.insert(0, val)`): $O(N)$, так как весь массив сдвигается в памяти через `memmove`!

`collections.deque` — это **двусвязный список блоков фиксированного размера** (по 64 элемента в блоке):
- `.append()` и `.appendleft()`: строго $O(1)$.
- `.pop()` и `.popleft()`: строго $O(1)$.
- Параметр `maxlen`: автоматическое вытеснение старых элементов без оверхеда.

### Задание:
Реализуйте класс `SlidingWindowStats(window_size: int)`:
- Хранит последние `window_size` числовых значений.
- При превышении размера старые значения должны вытесняться за $O(1)$.
- Метод `add(val: float) -> None`: добавляет число.
- Метод `get_mean() -> float`: возвращает среднее арифметическое (округленное до 2 знаков) или 0.0 при пустом окне.
- Метод `get_variance() -> float`: возвращает дисперсию $\\frac{\\sum (x - \\mu)^2}{N}$ (округленную до 2 знаков) или 0.0.
- Метод `is_full() -> bool`: возвращает True, если окно заполнено на `window_size`.
""",
            "task_description": "Реализуйте эффективный класс скользящего окна `SlidingWindowStats` на базе `collections.deque`.",
            "starter_code": """from collections import deque

class SlidingWindowStats:
    \"\"\"
    Эффективное скользящее окно с вычислением статистик за O(1) / O(K).
    \"\"\"
    def __init__(self, window_size: int):
        # TODO: Инициализируйте deque с maxlen
        pass

    def add(self, val: float) -> None:
        pass

    def get_mean(self) -> float:
        pass

    def get_variance(self) -> float:
        pass

    def is_full(self) -> bool:
        pass
""",
            "hints": [
                {
                    "level": 1,
                    "title": "Концептуальная наводка",
                    "content": "Используйте `self.buffer = deque(maxlen=window_size)`. При добавлении элементов deque с maxlen автоматически удаляет самый старый элемент слева!"
                },
                {
                    "level": 2,
                    "title": "Математические расчеты",
                    "content": "Среднее: mean = sum(self.buffer) / len(self.buffer). Дисперсия: sum((x - mean)**2 for x in self.buffer) / len(self.buffer)."
                },
                {
                    "level": 3,
                    "title": "Оптимизация и обработка граничных случаев",
                    "content": "Не забудьте обработать пустой буфер: если len(self.buffer) == 0, возвращайте 0.0. Округляйте результаты через round(val, 2)."
                }
            ],
            "solution": """from collections import deque

class SlidingWindowStats:
    \"\"\"
    Высокопроизводительное скользящее окно фиксированного размера.
    Использует collections.deque с ограничением длины (maxlen).
    \"\"\"
    def __init__(self, window_size: int):
        if window_size <= 0:
            raise ValueError("Window size must be positive")
        self.window_size = window_size
        self._buffer: deque[float] = deque(maxlen=window_size)

    def add(self, val: float) -> None:
        self._buffer.append(float(val))

    def get_mean(self) -> float:
        if not self._buffer:
            return 0.0
        return round(sum(self._buffer) / len(self._buffer), 2)

    def get_variance(self) -> float:
        if not self._buffer:
            return 0.0
        mean = sum(self._buffer) / len(self._buffer)
        var = sum((x - mean) ** 2 for x in self._buffer) / len(self._buffer)
        return round(var, 2)

    def is_full(self) -> bool:
        return len(self._buffer) == self.window_size
""",
            "test_suite_code": """
@pydeep_test("Проверка скользящего окна и автовытеснения")
def test_window_eviction():
    sw = SlidingWindowStats(window_size=3)
    assert not sw.is_full()
    sw.add(10.0)
    sw.add(20.0)
    sw.add(30.0)
    assert sw.is_full()
    assert sw.get_mean() == 20.0
    
    # Добавляем 4-й элемент -> 10.0 вытесняется, остаются 20, 30, 40
    sw.add(40.0)
    assert sw.is_full()
    assert sw.get_mean() == 30.0
    return True

@pydeep_test("Проверка вычисления дисперсии")
def test_variance():
    sw = SlidingWindowStats(window_size=2)
    sw.add(10.0)
    sw.add(20.0)
    # Mean = 15, Var = ((10-15)^2 + (20-15)^2) / 2 = (25 + 25) / 2 = 25.0
    assert sw.get_variance() == 25.0
    return True

@pydeep_test("Граничный случай: пустое окно")
def test_empty_window():
    sw = SlidingWindowStats(window_size=5)
    assert sw.get_mean() == 0.0
    assert sw.get_variance() == 0.0
    assert not sw.is_full()
    return True
"""
        }
    ]
}
