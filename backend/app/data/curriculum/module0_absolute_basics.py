"""
Module 0: Absolute Python Basics (Zero to Hero)
Designed for true beginners: Variables, print, f-strings, if/else, loops, and basic dicts.
Provides an ultra-smooth, encouraging on-ramp before intermediate topics.
"""

MODULE_0 = {
    "id": "module_0",
    "title": "Модуль 0: Абсолютный старт с нуля",
    "description": "Первые шаги в Python: переменные, вывод print, f-строки, условия if/else, циклы for и базовые структуры.",
    "order": 0,
    "lessons": [
        {
            "id": "m0_l1_variables_io",
            "title": "0.1. Переменные, вычисления и вывод (print, f-строки)",
            "difficulty": "beginner",
            "estimated_minutes": 10,
            "theory_md": """# Первые шаги в Python: Переменные и Вывод

Добро пожаловать в мир Python! Если вы только начинаете путь в программировании — этот модуль создан специально для вас.

### 1. Что такое переменная?

Переменная — это именованная ячейка в памяти компьютера. Мы даем переменной понятное имя и сохраняем в неё значение через оператор присваивания `=`:

```python
item_name = "Книга"   # Текст (строка, str) — пишется в кавычках
price = 500           # Целое число (int)
quantity = 2          # Количество (int)
```

### 2. Арифметические операции

Python выполняет математические вычисления как калькулятор:
- `+` сложение: `10 + 5` -> `15`
- `-` вычитание: `10 - 5` -> `5`
- `*` умножение: `10 * 5` -> `50`
- `/` деление: `10 / 2` -> `5.0`

### 3. Форматирование строк (f-строки)

В современном Python самый удобный способ объединять текст и переменные — это **f-строки** (f-strings). Перед строкой ставится буква `f`, а имена переменных или выражения пишутся внутри фигурных скобок `{}`:

```python
name = "Анна"
points = 100
message = f"Привет, {name}! У вас {points} баллов."
# message станет строкой: "Привет, Анна! У вас 100 баллов."
```

### 4. Функция и оператор `return`

Функция получает входные данные (параметры), выполняет вычисления и **возвращает** результат с помощью оператора `return`:

```python
def multiply(a: int, b: int) -> int:
    result = a * b
    return result
```

---

### Задание:
Напишите функцию `calculate_order(item_name: str, price: int, quantity: int) -> str`:
1. Вычислите общую стоимость: перемножьте цену `price` и количество `quantity`.
2. Сформируйте и верните строку по шаблону:
   `f"Заказ: {item_name} | Итого: {total} руб."`
""",
            "task_description": "Реализуйте функцию `calculate_order(item_name: str, price: int, quantity: int) -> str`, вычисляющую стоимость заказа и возвращающую отформатированную строку чека.",
            "starter_code": """def calculate_order(item_name: str, price: int, quantity: int) -> str:
    \"\"\"
    Рассчитывает общую стоимость покупки и формирует строку заказа.
    \"\"\"
    # TODO: Рассчитайте стоимость заказа (цена умноженная на количество)
    # TODO: Сформируйте и верните строку заказа в формате f-строки
    pass
""",
            "hints": [
                {
                    "level": 1,
                    "title": "С чего начать",
                    "content": "Создайте переменную (например, `total`), в которую сохраните результат умножения цены `price` на количество `quantity` с помощью знака `*`."
                },
                {
                    "level": 2,
                    "title": "Как вернуть f-строку",
                    "content": "Используйте ключевое слово `return` и букву `f` перед кавычками: `return f\"Заказ: {item_name} | Итого: {total} руб.\"`."
                },
                {
                    "level": 3,
                    "title": "Готовое решение",
                    "content": "```python\ntotal = price * quantity\nreturn f\"Заказ: {item_name} | Итого: {total} руб.\"\n```"
                }
            ],
            "solution": """def calculate_order(item_name: str, price: int, quantity: int) -> str:
    \"\"\"
    Эталонное решение:
    Вычисляем произведение цены и количества, возвращаем форматированную строку.
    \"\"\"
    total = price * quantity
    return f"Заказ: {item_name} | Итого: {total} руб."
""",
            "test_suite_code": """
@pydeep_test("Базовый заказ 1 товара")
def test_single_item():
    res = calculate_order("Ноутбук", 50000, 1)
    expected = "Заказ: Ноутбук | Итого: 50000 руб."
    assert res == expected, f"Ожидалось: '{expected}', получено: '{res}'"
    return True

@pydeep_test("Заказ нескольких единиц товара")
def test_multiple_items():
    res = calculate_order("Кофе", 150, 3)
    expected = "Заказ: Кофе | Итого: 450 руб."
    assert res == expected, f"Ожидалось: '{expected}', получено: '{res}'"
    return True

@pydeep_test("Нулевое количество")
def test_zero_quantity():
    res = calculate_order("Блокнот", 200, 0)
    expected = "Заказ: Блокнот | Итого: 0 руб."
    assert res == expected, f"Ожидалось: '{expected}', получено: '{res}'"
    return True
"""
        },
        {
            "id": "m0_l2_conditionals",
            "title": "0.2. Ветвления и логика (if, elif, else)",
            "difficulty": "beginner",
            "estimated_minutes": 10,
            "theory_md": """# Ветвления в Python: if, elif, else

Программы должны уметь принимать решения в зависимости от входных данных. Для этого используется конструкция `if / elif / else`.

### 1. Операторы сравнения
- `>` строго больше (`5 > 3` -> `True`)
- `<` строго меньше (`2 < 1` -> `False`)
- `>=` больше либо равно
- `<=` меньше либо равно
- `==` проверка на равенство (два знака равно!)
- `!=` проверка на неравенство

### 2. Синтаксис условий:
В Python блоки кода внутри условий выделяются **отступами** (4 пробела):

```python
temperature = 22

if temperature > 25:
    status = "Жарко"
elif temperature >= 15:
    status = "Комфортно"
else:
    status = "Холодно"
```

Инструкция `elif` (сокращение от *else if*) проверяется по цепочке сверху вниз только в том случае, если все предыдущие проверки вернули `False`. Блок `else` выполняется, если ни одно из условий выше не подошло.

---

### Задание:
Напишите функцию `classify_speed(speed: int) -> str`, которая определяет скоростной режим:
- Если `speed < 0` -> вернуть `"ошибка"` (скорость не может быть отрицательной)
- Если `speed == 0` -> вернуть `"стоит"`
- Если `speed <= 60` -> вернуть `"город"`
- Если `speed <= 110` -> вернуть `"трасса"`
- Во всех остальных случаях (`speed > 110`) -> вернуть `"превышение"`
""",
            "task_description": "Реализуйте функцию `classify_speed(speed: int) -> str` с каскадом проверок if/elif/else.",
            "starter_code": """def classify_speed(speed: int) -> str:
    \"\"\"
    Определяет скоростной режим автомобиля.
    \"\"\"
    # TODO: Проверьте скорость и верните подходящую категорию:
    # отрицательная -> 'ошибка', 0 -> 'стоит', до 60 -> 'город', до 110 -> 'трасса', свыше 110 -> 'превышение'
    pass
""",
            "hints": [
                {
                    "level": 1,
                    "title": "Порядок условий",
                    "content": "Начните с проверки на отрицательную скорость `if speed < 0:`, затем проверяйте `elif speed == 0:`."
                },
                {
                    "level": 2,
                    "title": "Проверка диапазонов",
                    "content": "Поскольку условия проверяются сверху вниз, после нуля достаточно проверить `elif speed <= 60:`, а затем `elif speed <= 110:`."
                },
                {
                    "level": 3,
                    "title": "Фрагмент решения",
                    "content": "```python\nif speed < 0:\n    return 'ошибка'\nelif speed == 0:\n    return 'стоит'\nelif speed <= 60:\n    return 'город'\nelif speed <= 110:\n    return 'трасса'\nelse:\n    return 'превышение'\n```"
                }
            ],
            "solution": """def classify_speed(speed: int) -> str:
    \"\"\"
    Классификация скорости через цепочку if-elif-else.
    \"\"\"
    if speed < 0:
        return "ошибка"
    elif speed == 0:
        return "стоит"
    elif speed <= 60:
        return "город"
    elif speed <= 110:
        return "трасса"
    else:
        return "превышение"
""",
            "test_suite_code": """
@pydeep_test("Проверка отрицательной скорости")
def test_negative():
    assert classify_speed(-10) == "ошибка"
    return True

@pydeep_test("Проверка стоящей машины (0 км/ч)")
def test_standing():
    assert classify_speed(0) == "стоит"
    return True

@pydeep_test("Проверка городского режима")
def test_city():
    assert classify_speed(40) == "город"
    assert classify_speed(60) == "город"
    return True

@pydeep_test("Проверка трассы")
def test_highway():
    assert classify_speed(90) == "трасса"
    assert classify_speed(110) == "трасса"
    return True

@pydeep_test("Проверка превышения")
def test_speeding():
    assert classify_speed(130) == "превышение"
    return True
"""
        },
        {
            "id": "m0_l3_loops_lists",
            "title": "0.3. Списки и циклы (for, append, filter)",
            "difficulty": "beginner",
            "estimated_minutes": 15,
            "theory_md": """# Списки и Циклы в Python

Список (`list`) — это упорядоченная коллекция элементов. В Python списки записываются в квадратных скобках `[]`.

### 1. Создание списка и добавление элементов:
```python
fruits = ["яблоко", "банан", "груша"]
fruits.append("апельсин")  # метод .append() добавляет элемент в конец списка
print(len(fruits))         # функция len() возвращает длину списка (4)
```

### 2. Цикл `for`
Цикл `for` позволяет обойти каждый элемент списка по очереди:

```python
numbers = [1, 2, 3, 4, 5]
for num in numbers:
    print(f"Текущее число: {num}")
```

### 3. Проверка четности числа:
Остаток от деления `%` на 2 позволяет легко проверить, четное ли число:
```python
if num % 2 == 0:
    # Число делится на 2 без остатка — значит, оно четное!
```

---

### Задание:
Напишите функцию `filter_evens(numbers: list[int]) -> list[int]`:
1. Принимает список чисел `numbers`.
2. Создает новый пустой список для четных чисел.
3. Проходится циклом `for` по входному списку: если число четное (`num % 2 == 0`), добавляет его в результирующий список методом `.append()`.
4. Возвращает список отобранных четных чисел. Если четных чисел нет или список пустой — возвращает пустой список `[]`.
""",
            "task_description": "Реализуйте функцию `filter_evens(numbers: list[int]) -> list[int]`, которая отбирает только четные числа в новый список.",
            "starter_code": """def filter_evens(numbers: list[int]) -> list[int]:
    \"\"\"
    Отбирает четные числа из переданного списка.
    \"\"\"
    # TODO: Подготовьте пустой список для сохранения четных чисел
    # TODO: Обойдите входные числа циклом for и добавьте четные в подготовленный список
    # TODO: Верните результирующий список
    pass
""",
            "hints": [
                {
                    "level": 1,
                    "title": "Создание списка",
                    "content": "Перед циклом создайте переменную для результата: `evens = []`."
                },
                {
                    "level": 2,
                    "title": "Проверка и добавление",
                    "content": "Внутри цикла используйте условие `if num % 2 == 0:` и добавляйте элемент в список: `evens.append(num)`."
                },
                {
                    "level": 3,
                    "title": "Полный код решения",
                    "content": "```python\nevens = []\nfor num in numbers:\n    if num % 2 == 0:\n        evens.append(num)\nreturn evens\n```"
                }
            ],
            "solution": """def filter_evens(numbers: list[int]) -> list[int]:
    \"\"\"
    Отбираем четные элементы списка.
    \"\"\"
    evens = []
    for num in numbers:
        if num % 2 == 0:
            evens.append(num)
    return evens
""",
            "test_suite_code": """
@pydeep_test("Смешанный список четных и нечетных")
def test_mixed():
    res = filter_evens([1, 2, 3, 4, 5, 6])
    assert res == [2, 4, 6], f"Ожидалось [2, 4, 6], получено: {res}"
    return True

@pydeep_test("Только нечетные числа")
def test_only_odds():
    res = filter_evens([1, 3, 5, 7])
    assert res == [], f"Ожидался пустой список, получено: {res}"
    return True

@pydeep_test("Пустой входной список")
def test_empty():
    res = filter_evens([])
    assert res == [], f"Ожидался пустой список, получено: {res}"
    return True
"""
        },
        {
            "id": "m0_l4_dictionaries",
            "title": "0.4. Словари и подсчет данных (dict, ключ-значение)",
            "difficulty": "beginner",
            "estimated_minutes": 15,
            "theory_md": """# Словари в Python (dict)

Словарь — это структура данных, хранящая пары **«ключ: значение»**.

### 1. Создание словаря и доступ по ключу:
```python
user = {
    "name": "Анна",
    "city": "Москва",
    "age": 28
}

print(user["name"])  # "Анна"
user["city"] = "Казань"  # Изменение значения по ключу
user["job"] = "Python Developer"  # Добавление новой пары ключ:значение
```

### 2. Проверка наличия ключа:
Оператор `in` проверяет, есть ли ключ в словаре:
```python
if "email" in user:
    print("Email найден")
else:
    print("Email отсутствует")
```

### 3. Подсчет частоты элементов:
Словари идеально подходят для подсчета количества повторений:

```python
words = ["яблоко", "груша", "яблоко"]
counts = {}

for w in words:
    if w in counts:
        counts[w] += 1
    else:
        counts[w] = 1

print(counts)  # {'яблоко': 2, 'груша': 1}
```

---

### Задание:
Напишите функцию `count_words(words: list[str]) -> dict[str, int]`:
1. Принимает список слов `words`.
2. Каждое слово приводит к нижнему регистру методом `.lower()`.
3. Считает, сколько раз каждое слово встретилось в списке.
4. Возвращает словарь с количеством повторений каждого слова.
""",
            "task_description": "Реализуйте функцию `count_words(words: list[str]) -> dict[str, int]`, которая приводит слова к нижнему регистру и подсчитывает частоту каждого слова.",
            "starter_code": """def count_words(words: list[str]) -> dict[str, int]:
    \"\"\"
    Считает количество повторений каждого слова (в нижнем регистре).
    \"\"\"
    # TODO: Инициализируйте словарь для подсчета частот
    # TODO: Обойдите слова, приведите каждое к нижнему регистру и обновите счетчик
    # TODO: Верните словарь с результатами
    pass
""",
            "hints": [
                {
                    "level": 1,
                    "title": "Нижний регистр",
                    "content": "Для перевода слова в нижний регистр используйте метод `word.lower()`."
                },
                {
                    "level": 2,
                    "title": "Логика подсчета",
                    "content": "Проверяйте: если очищенное слово уже есть в словаре `if clean in counts: counts[clean] += 1`, иначе инициализируйте счетчик единицей `counts[clean] = 1`."
                },
                {
                    "level": 3,
                    "title": "Метод get() или готовый цикл",
                    "content": "```python\ncounts = {}\nfor word in words:\n    clean = word.lower()\n    counts[clean] = counts.get(clean, 0) + 1\nreturn counts\n```"
                }
            ],
            "solution": """def count_words(words: list[str]) -> dict[str, int]:
    \"\"\"
    Подсчет частоты слов с приведением к нижнему регистру.
    \"\"\"
    counts = {}
    for word in words:
        clean = word.lower()
        counts[clean] = counts.get(clean, 0) + 1
    return counts
""",
            "test_suite_code": """
@pydeep_test("Подсчет с разным регистром букв")
def test_case_insensitive():
    res = count_words(["Python", "python", "PYTHON", "code"])
    assert res == {"python": 3, "code": 1}, f"Получено: {res}"
    return True

@pydeep_test("Список из уникальных слов")
def test_unique():
    res = count_words(["a", "b", "c"])
    assert res == {"a": 1, "b": 1, "c": 1}
    return True

@pydeep_test("Пустой список")
def test_empty():
    res = count_words([])
    assert res == {}
    return True
"""
        }
    ]
}
