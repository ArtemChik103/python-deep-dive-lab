"""
Module 1: Foundation Tools
Strings, slices, *args/**kwargs, comprehensions, and error handling.
Bridges the gap between absolute basics and intermediate Python.
"""

MODULE_FOUNDATION_TOOLS = {
    "id": "module_foundation_tools",
    "title": "Модуль 1: Базовые инструменты языка",
    "description": "Срезы строк [start:stop:step], распаковка *args/**kwargs, лаконичные comprehensions и обработка исключений try/except.",
    "order": 1,
    "lessons": [
        {
            "id": "m1_f1_strings_slices",
            "title": "1.1. Строки, срезы [start:stop:step] и методы строк",
            "difficulty": "beginner",
            "estimated_minutes": 15,
            "theory_md": """# Строки и Срезы в Python

Строка (`str`) в Python — это **неизменяемая** последовательность символов с поддержкой мощного синтаксиса срезов (slices).

### 1. Синтаксис срезов: `sequence[start:stop:step]`
- `start`: индекс начала (включительно, по умолчанию `0`).
- `stop`: индекс окончания (не включая, по умолчанию длина строки).
- `step`: шаг обхода (по умолчанию `1`).

```python
s = "Python3"
print(s[0:6])    # "Python"
print(s[::2])     # "Pto3" (каждый второй символ)
print(s[::-1])    # "3nohtyP" (разворот строки!)
```

### 2. Отрицательные индексы
Отрицательные числа ведут отсчет с конца строки:
- `s[-1]` — последний символ
- `s[:-1]` — вся строка без последнего символа

### 3. Полезные методы строк:
- `.strip()` — удаляет пробелы и переводы строк по краям
- `.split(separator)` — разбивает строку в список подстрок
- `.join(iterable)` — объединяет список строк через разделитель: `"-".join(["a", "b"])` -> `"a-b"`
- `.replace(old, new)` — заменяет подстроку

---

### Задание:
Напишите функцию `create_slug(title: str, max_words: int = 5) -> str`:
1. Принимает заголовок статьи `title`.
2. Убирает лишние пробелы по краям (`.strip()`) и переводит в нижний регистр (`.lower()`).
3. Разбивает текст на отдельные слова (`.split()`).
4. Если слов больше чем `max_words`, берет только первые `max_words` слов (используя срез `[:max_words]`).
5. Соединяет полученные слова через дефис `-` с помощью `"-".join(...)`.
6. Возвращает получившийся slug.
""",
            "task_description": "Реализуйте функцию `create_slug(title: str, max_words: int = 5) -> str` для создания URL-slug из заголовка с использованием срезов и методов строк.",
            "starter_code": """def create_slug(title: str, max_words: int = 5) -> str:
    \"\"\"
    Преобразует строку заголовка в URL-совместимый slug.
    \"\"\"
    # TODO: Приведите к нижнему регистру и удалите пробелы по краям
    # TODO: Разбейте на слова через .split()
    # TODO: Возьмите срез первых max_words слов
    # TODO: Объедините слова через дефис '-'
    pass
""",
            "hints": [
                {
                    "level": 1,
                    "title": "Нормализация",
                    "content": "Используйте `words = title.strip().lower().split()`, чтобы получить список очищенных слов."
                },
                {
                    "level": 2,
                    "title": "Ограничение срезом",
                    "content": "Срез `selected_words = words[:max_words]` безопасно вернет не более `max_words` слов, даже если в тексте их меньше."
                },
                {
                    "level": 3,
                    "title": "Объединение",
                    "content": "Используйте `'-'.join(selected_words)` и верните результат."
                }
            ],
            "solution": """def create_slug(title: str, max_words: int = 5) -> str:
    \"\"\"
    Генерация slug с помощью срезов и строковых методов.
    \"\"\"
    words = title.strip().lower().split()
    selected = words[:max_words]
    return "-".join(selected)
""",
            "test_suite_code": """
@pydeep_test("Базовый заголовок из трех слов")
def test_simple_slug():
    res = create_slug("Learn Python Fast")
    assert res == "learn-python-fast", f"Получено: {res}"
    return True

@pydeep_test("Ограничение по max_words")
def test_max_words_limit():
    res = create_slug("The quick brown fox jumps over the lazy dog", max_words=4)
    assert res == "the-quick-brown-fox", f"Получено: {res}"
    return True

@pydeep_test("Лишние пробелы и разный регистр")
def test_whitespace_and_casing():
    res = create_slug("   DEEP  dive   Into Code   ")
    assert res == "deep-dive-into-code", f"Получено: {res}"
    return True

@pydeep_test("Пустая строка")
def test_empty():
    res = create_slug("")
    assert res == "", f"Получено: '{res}'"
    return True
"""
        },
        {
            "id": "m1_f2_functions_args_kwargs",
            "title": "1.2. Функции: позиционные аргументы, *args и **kwargs",
            "difficulty": "beginner",
            "estimated_minutes": 15,
            "theory_md": """# Продвинутые аргументы функций: `*args` и `**kwargs`

Функции в Python могут принимать переменное число аргументов:
1. `*args` (arbitrary positional arguments) — упаковывает все лишние позиционные аргументы в **кортеж (tuple)**.
2. `**kwargs` (arbitrary keyword arguments) — упаковывает все именованные аргументы в **словарь (dict)**.

```python
def print_everything(required_arg, *args, **kwargs):
    print("Обязательный:", required_arg)
    print("Кортеж args:", args)
    print("Словарь kwargs:", kwargs)

print_everything("hello", 1, 2, 3, mode="strict", debug=True)
# args -> (1, 2, 3)
# kwargs -> {'mode': 'strict', 'debug': True}
```

### Значения по умолчанию
Аргументы со значениями по умолчанию должны следовать **после** обязательных позиционных аргументов:
```python
def greet(name, greeting="Привет"):
    return f"{greeting}, {name}!"
```

---

### Задание:
Напишите функцию `calculate_invoice(base_amount: float, *fees: float, tax_rate: float = 0.0, **metadata) -> dict`:
1. Принимает базовую сумму `base_amount`.
2. `*fees`: произвольное число дополнительных комиссий или сборов (float). Если комиссии не переданы, их сумма равна `0.0`.
3. `tax_rate`: процент налога в долях единицы (по умолчанию `0.0`, например `0.1` это 10%).
4. `subtotal` = `base_amount + sum(fees)`.
5. `tax_amount` = `subtotal * tax_rate`.
6. `total` = `round(subtotal + tax_amount, 2)`.
7. Функция должна возвращать словарь:
   `{"subtotal": round(subtotal, 2), "tax": round(tax_amount, 2), "total": total, "meta": metadata}`
""",
            "task_description": "Реализуйте функцию `calculate_invoice(base_amount: float, *fees: float, tax_rate: float = 0.0, **metadata) -> dict` с использованием *args и **kwargs.",
            "starter_code": """def calculate_invoice(base_amount: float, *fees: float, tax_rate: float = 0.0, **metadata) -> dict:
    \"\"\"
    Рассчитывает счет фактуру с учетом комиссий, налогов и произвольных метаданных.
    \"\"\"
    # TODO: Вычислите subtotal (базовая сумма + сумма всех fees)
    # TODO: Вычислите tax_amount (subtotal * tax_rate)
    # TODO: Вычислите total (subtotal + tax_amount) с округлением round(..., 2)
    # TODO: Верните словарь с полями subtotal, tax, total, meta
    pass
""",
            "hints": [
                {
                    "level": 1,
                    "title": "Суммирование fees",
                    "content": "Кортеж `fees` можно сложить встроенной функцией: `total_fees = sum(fees)`."
                },
                {
                    "level": 2,
                    "title": "Формулы",
                    "content": "`subtotal = base_amount + sum(fees)`, затем `tax = subtotal * tax_rate`, а `total = subtotal + tax`."
                },
                {
                    "level": 3,
                    "title": "Структура возврата",
                    "content": "```python\nsubtotal = base_amount + sum(fees)\ntax = subtotal * tax_rate\ntotal = subtotal + tax\nreturn {\n    'subtotal': round(subtotal, 2),\n    'tax': round(tax, 2),\n    'total': round(total, 2),\n    'meta': metadata\n}\n```"
                }
            ],
            "solution": """def calculate_invoice(base_amount: float, *fees: float, tax_rate: float = 0.0, **metadata) -> dict:
    \"\"\"
    Универсальный расчет счета с использованием *args и **kwargs.
    \"\"\"
    subtotal = base_amount + sum(fees)
    tax = subtotal * tax_rate
    total = subtotal + tax
    return {
        "subtotal": round(subtotal, 2),
        "tax": round(tax, 2),
        "total": round(total, 2),
        "meta": metadata
    }
""",
            "test_suite_code": """
@pydeep_test("Базовый расчет без комиссий и налога")
def test_simple_invoice():
    res = calculate_invoice(1000.0)
    assert res["subtotal"] == 1000.0
    assert res["tax"] == 0.0
    assert res["total"] == 1000.0
    assert res["meta"] == {}
    return True

@pydeep_test("Расчет с комиссиями через *args")
def test_with_fees():
    res = calculate_invoice(500.0, 50.0, 25.0, 25.0)
    assert res["subtotal"] == 600.0
    assert res["total"] == 600.0
    return True

@pydeep_test("Расчет с налогом и метаданными **kwargs")
def test_tax_and_kwargs():
    res = calculate_invoice(100.0, tax_rate=0.2, client="ООО Вектор", invoice_id=42)
    assert res["subtotal"] == 100.0
    assert res["tax"] == 20.0
    assert res["total"] == 120.0
    assert res["meta"] == {"client": "ООО Вектор", "invoice_id": 42}
    return True
"""
        },
        {
            "id": "m1_f3_comprehensions",
            "title": "1.3. Списковые и словарные включения (Comprehensions)",
            "difficulty": "beginner",
            "estimated_minutes": 15,
            "theory_md": """# Списковые включения (List & Dict Comprehensions)

Comprehensions (генераторы коллекций) — визитная карточка лаконичного и быстрого Python-кода. Они заменяют громоздкие циклы `for` с `.append()` одной выразительной строкой.

### 1. List Comprehension:
Синтаксис: `[выражение for элемент in коллекция if условие]`

```python
# Вместо этого:
evens = []
for x in range(10):
    if x % 2 == 0:
        evens.append(x ** 2)

# Мы пишем так:
evens = [x ** 2 for x in range(10) if x % 2 == 0]
# [0, 4, 16, 36, 64]
```

### 2. Dict Comprehension:
Синтаксис: `{ключ: значение for элемент in коллекция if условие}`

```python
names = ["Анна", "Борис", "Владимир"]
name_lengths = {name: len(name) for name in names}
# {'Анна': 4, 'Борис': 5, 'Владимир': 8}
```

---

### Задание:
Напишите функцию `filter_and_transform_users(users: list[dict], min_age: int = 18) -> dict[str, str]`:
1. Принимает список словарей пользователей `users`. Каждый словарь содержит: `{"id": "u1", "name": "Иван", "age": 20, "city": "Москва"}`.
2. С помощью **Dict Comprehension** отберите только пользователей с `age >= min_age`.
3. Сформируйте словарь, где:
   - Ключ — это `id` пользователя.
   - Значение — форматированная строка: `f"{name} ({city})"`.
4. Верните получившийся словарь.
""",
            "task_description": "Реализуйте функцию `filter_and_transform_users(users: list[dict], min_age: int = 18) -> dict[str, str]` с помощью словарного включения (Dict Comprehension).",
            "starter_code": """def filter_and_transform_users(users: list[dict], min_age: int = 18) -> dict[str, str]:
    \"\"\"
    Фильтрует совершеннолетних пользователей и преобразует в словарь {id: 'Имя (Город)'}.
    \"\"\"
    # TODO: Реализуйте с помощью Dict Comprehension в одну строку:
    # {u['id']: f"{u['name']} ({u['city']})" for u in users if u['age'] >= min_age}
    pass
""",
            "hints": [
                {
                    "level": 1,
                    "title": "Синтаксис включения",
                    "content": "Используйте шаблон: `{u['id']: ... for u in users if u['age'] >= min_age}`."
                },
                {
                    "level": 2,
                    "title": "Форматирование значения",
                    "content": "Значением словаря должна быть f-строка: `f\"{u['name']} ({u['city'])}\"`."
                },
                {
                    "level": 3,
                    "title": "Готовый код функции",
                    "content": "```python\nreturn {\n    u['id']: f\"{u['name']} ({u['city'])}\"\n    for u in users\n    if u['age'] >= min_age\n}\n```"
                }
            ],
            "solution": """def filter_and_transform_users(users: list[dict], min_age: int = 18) -> dict[str, str]:
    \"\"\"
    Элегантная трансформация данных через Dict Comprehension.
    \"\"\"
    return {
        u["id"]: f"{u['name']} ({u['city']})"
        for u in users
        if u["age"] >= min_age
    }
""",
            "test_suite_code": """
@pydeep_test("Фильтрация несовершеннолетних пользователей")
def test_age_filtering():
    data = [
        {"id": "u1", "name": "Анна", "age": 22, "city": "Москва"},
        {"id": "u2", "name": "Михаил", "age": 16, "city": "СПб"},
        {"id": "u3", "name": "Ольга", "age": 30, "city": "Казань"}
    ]
    res = filter_and_transform_users(data, min_age=18)
    expected = {
        "u1": "Анна (Москва)",
        "u3": "Ольга (Казань)"
    }
    assert res == expected, f"Ожидалось {expected}, получено: {res}"
    return True

@pydeep_test("Все пользователи младше min_age")
def test_none_pass():
    data = [{"id": "u1", "name": "Илья", "age": 14, "city": "Пермь"}]
    res = filter_and_transform_users(data, min_age=18)
    assert res == {}
    return True

@pydeep_test("Пустой список пользователей")
def test_empty():
    assert filter_and_transform_users([]) == {}
    return True
"""
        },
        {
            "id": "m1_f4_exceptions_handling",
            "title": "1.4. Обработка ошибок: try, except, raise и finally",
            "difficulty": "beginner",
            "estimated_minutes": 15,
            "theory_md": """# Обработка исключений в Python

Ошибки во время выполнения программы называются **исключениями (Exceptions)**. Без их обработки программа аварийно завершается (crash).

### 1. Блок `try ... except`:
```python
try:
    number = int("не число")
except ValueError as e:
    print("Не удалось преобразовать в число:", e)
```

### 2. Типичные стандартные исключения:
- `ValueError`: неподходящее значение аргумента (например `int("abc")`)
- `KeyError`: попытка взять несуществующий ключ из словаря
- `IndexError`: обращение по индексу за пределами списка
- `ZeroDivisionError`: деление на ноль
- `TypeError`: операция над несовместимыми типами

### 3. Блоки `else` и `finally`:
- `else`: выполняется, только если в блоке `try` **не возникло** ошибок.
- `finally`: выполняется **всегда**, даже если произошла ошибка или выполнен `return`.

### 4. Генерация собственных исключений: `raise`
```python
if balance < amount:
    raise ValueError("Недостаточно средств на счете")
```

---

### Задание:
Напишите функцию `safe_parse_config(raw_items: list[str]) -> tuple[dict[str, int], list[str]]`:
1. На вход подается список строк вида `"key=value"`, например `["port=8080", "workers=4", "invalid_entry", "timeout=abc"]`.
2. Функция должна разобрать каждую строку:
   - Разбить строку по первому символу `=` на две части: `key, val = item.split("=", 1)`. Если символа `=` нет, возникнет `ValueError`.
   - Преобразовать значение `val` в целое число `int(val.strip())`. Если там не число, возникнет `ValueError`.
3. Успешно разобранные пары добавьте в результирующий словарь `config: dict[str, int]`.
4. Строки, которые не удалось разобрать (из-за отсутствия `=` или некорректного числа), добавьте в список ошибок `errors: list[str]`.
5. Верните кортеж: `(config, errors)`.
""",
            "task_description": "Реализуйте функцию `safe_parse_config(raw_items: list[str]) -> tuple[dict[str, int], list[str]]` с безопасным перехватом ValueError через try-except.",
            "starter_code": """def safe_parse_config(raw_items: list[str]) -> tuple[dict[str, int], list[str]]:
    \"\"\"
    Парсит настройки конфигурации формата key=int_value с перехватом ошибок.
    Возвращает (словарь_конфига, список_ошибочных_строк).
    \"\"\"
    config = {}
    errors = []
    # TODO: Пройдитесь по raw_items в цикле
    # TODO: В блоке try разделите строку по '=' и сконвертируйте в int
    # TODO: В блоке except ValueError добавьте строку в errors
    # TODO: Верните config, errors
    pass
""",
            "hints": [
                {
                    "level": 1,
                    "title": "Структура try-except",
                    "content": "Внутри цикла `for item in raw_items:` оберните парсинг в блок `try: ... except ValueError: errors.append(item)`."
                },
                {
                    "level": 2,
                    "title": "Разбиение строки",
                    "content": "Проверьте: `key, val = item.split('=', 1)` — если знака равенства нет, это вызовет `ValueError` и автоматически уйдет в блок `except`."
                },
                {
                    "level": 3,
                    "title": "Преобразование в int",
                    "content": "`config[key.strip()] = int(val.strip())` — если `val` не число, это также вызовет `ValueError`."
                }
            ],
            "solution": """def safe_parse_config(raw_items: list[str]) -> tuple[dict[str, int], list[str]]:
    \"\"\"
    Безопасный парсинг конфигурации с перехватом исключений.
    \"\"\"
    config = {}
    errors = []
    for item in raw_items:
        try:
            parts = item.split("=", 1)
            if len(parts) != 2:
                raise ValueError("No delimiter")
            key, val = parts
            config[key.strip()] = int(val.strip())
        except ValueError:
            errors.append(item)
    return config, errors
""",
            "test_suite_code": """
@pydeep_test("Парсинг корректных и ошибочных строк")
def test_mixed_config():
    raw = ["port=8000", "retries=3", "debug=true", "no_equal_sign", "timeout=30"]
    config, errors = safe_parse_config(raw)
    assert config == {"port": 8000, "retries": 3, "timeout": 30}
    assert errors == ["debug=true", "no_equal_sign"]
    return True

@pydeep_test("Все строки валидны")
def test_all_valid():
    raw = ["a=1", "b=2"]
    config, errors = safe_parse_config(raw)
    assert config == {"a": 1, "b": 2}
    assert errors == []
    return True

@pydeep_test("Пустой входной список")
def test_empty():
    config, errors = safe_parse_config([])
    assert config == {}
    assert errors == []
    return True
"""
        }
    ]
}
