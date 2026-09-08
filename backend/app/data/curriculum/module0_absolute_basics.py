"""
Module 0: Absolute Python Basics (Zero to Hero)
Designed for true beginners: Variables, print, f-strings, if/else, loops, and basic dicts.
Provides an ultra-smooth on-ramp before diving into CPython memory internals.
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

Переменная — это именованный ярлык для данных в памяти компьютера. Мы даем переменной имя и сохраняем в неё значение через оператор присваивания `=`:

```python
name = "Алексей"   # Строка (str) — текст в кавычках
age = 25           # Целое число (int)
height = 1.78      # Вещественное число с плавающей точкой (float)
is_student = True  # Логический тип (bool) — True или False
```

### 2. Арифметические операции

Python умеет выполнять математические операции как калькулятор:
- `+` сложение: `10 + 5` -> `15`
- `-` вычитание: `10 - 5` -> `5`
- `*` умножение: `10 * 5` -> `50`
- `/` деление (всегда возвращает `float`): `10 / 4` -> `2.5`
- `//` целочисленное деление: `10 // 4` -> `2`
- `%` остаток от деления: `10 % 3` -> `1`

### 3. Форматирование строк (f-строки)

В современном Python самый удобный способ объединять текст и переменные — это **f-строки** (f-strings). Перед строкой ставится буква `f`, а имена переменных или выражения пишутся внутри фигурных скобок `{}`:

```python
item = "Книга"
price = 450
print(f"Товар: {item}, Стоимость: {price} руб.")
# Выведет: Товар: Книга, Стоимость: 450 руб.
```

Для округления чисел с плавающей точкой до двух знаков после запятой используется модификатор `:.2f`:
```python
total = 129.9
print(f"Итого: {total:.2f} руб.")
# Выведет: Итого: 129.90 руб.
```

---

### Задание:
Напишите функцию `calculate_order(item_name: str, price: float, quantity: int) -> str`:
1. Вычислите общую стоимость: умножьте цену `price` на количество `quantity`.
2. Верните отформатированную строку строго по шаблону:
   `f"Заказ: {item_name} | Количество: {quantity} | Итого: {total:.2f} руб."`
""",
            "task_description": "Реализуйте функцию `calculate_order(item_name: str, price: float, quantity: int) -> str`, вычисляющую стоимость заказа и возвращающую отформатированный чек с f-строкой.",
            "starter_code": """def calculate_order(item_name: str, price: float, quantity: int) -> str:
    \"\"\"
    Вычисляет общую сумму и возвращает отформатированную строку чека.
    \"\"\"
    # TODO: Вычислите total = price * quantity
    # TODO: Верните строку: f"Заказ: {item_name} | Количество: {quantity} | Итого: {total:.2f} руб."
    pass
""",
            "hints": [
                {
                    "level": 1,
                    "title": "С чего начать",
                    "content": "Создайте переменную total, в которую сохраните результат умножения цены на количество: `total = price * quantity`."
                },
                {
                    "level": 2,
                    "title": "Как вернуть f-строку",
                    "content": "Используйте ключевое слово `return` и букву `f` перед кавычками, например: `return f\"Заказ: {item_name} | ...\"`."
                },
                {
                    "level": 3,
                    "title": "Готовая строчка кода",
                    "content": "```python\ntotal = price * quantity\nreturn f\"Заказ: {item_name} | Количество: {quantity} | Итого: {total:.2f} руб.\"\n```"
                }
            ],
            "solution": """def calculate_order(item_name: str, price: float, quantity: int) -> str:
    \"\"\"
    Эталонное решение:
    Вычисляем произведение цены и количества, возвращаем форматированную строку.
    \"\"\"
    total = price * quantity
    return f"Заказ: {item_name} | Количество: {quantity} | Итого: {total:.2f} руб."
""",
            "test_suite_code": """
@pydeep_test("Базовый заказ 1 товара")
def test_single_item():
    res = calculate_order("Ноутбук", 50000.0, 1)
    expected = "Заказ: Ноутбук | Количество: 1 | Итого: 50000.00 руб."
    assert res == expected, f"Ожидалось: '{expected}', получено: '{res}'"
    return True

@pydeep_test("Заказ нескольких единиц товара с копейками")
def test_multiple_items():
    res = calculate_order("Кофе", 150.5, 3)
    expected = "Заказ: Кофе | Количество: 3 | Итого: 451.50 руб."
    assert res == expected, f"Ожидалось: '{expected}', получено: '{res}'"
    return True

@pydeep_test("Нулевое количество")
def test_zero_quantity():
    res = calculate_order("Блокнот", 200.0, 0)
    expected = "Заказ: Блокнот | Количество: 0 | Итого: 0.00 руб."
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

Программы должны уметь принимать решения в зависимости от условий. Для этого используется конструкция `if / elif / else`.

### 1. Операторы сравнения
- `>` строго больше (`5 > 3` -> `True`)
- `<` строго меньше (`2 < 1` -> `False`)
- `>=` больше либо равно
- `<=` меньше либо равно
- `==` проверка на равенство (не путать с одиночным `=` для присваивания!)
- `!=` проверка на неравенство

### 2. Синтаксис условий:
В Python блоки кода выделяются **отступами** (обычно 4 пробела):

```python
temperature = 22

if temperature > 25:
    print("Жарко")
elif temperature >= 15:
    print("Комфортно")
else:
    print("Холодно")
```

Инструкция `elif` (сокращение от *else if*) проверяется, только если предыдущий `if` оказался ложным (`False`). Блок `else` срабатывает, если ни одно из условий выше не подошло.

---

### Задание:
Напишите функцию `classify_speed(speed: int) -> str`, которая классифицирует скорость автомобиля:
- Если `speed < 0` -> вернуть `"ошибка"` (скорость не может быть отрицательной)
- Если `speed == 0` -> вернуть `"стоит"`
- Если `speed <= 60` -> вернуть `"город"`
- Если `speed <= 110` -> вернуть `"трасса"`
- Иначе (`speed > 110`) -> вернуть `"превышение"`
""",
            "task_description": "Реализуйте функцию `classify_speed(speed: int) -> str` с каскадом проверок if/elif/else.",
            "starter_code": """def classify_speed(speed: int) -> str:
    \"\"\"
    Определяет скоростной режим автомобиля.
    \"\"\"
    # TODO: Реализуйте проверки условий
    pass
""",
            "hints": [
                {
                    "level": 1,
                    "title": "Порядок условий",
                    "content": "Начните с проверки на отрицательную скорость `if speed < 0: return 'ошибка'`, затем проверяйте `speed == 0`."
                },
                {
                    "level": 2,
                    "title": "Проверка диапазонов",
                    "content": "Поскольку условия проверяются сверху вниз, после отсечения нуля достаточно написать `elif speed <= 60: return 'город'`, а затем `elif speed <= 110: return 'трасса'`."
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
            "title": "0.3. Списки и циклы (for, range, append)",
            "difficulty": "beginner",
            "estimated_minutes": 15,
            "theory_md": """# Списки и Циклы в Python

Списки (`list`) позволяют хранить упорядоченные коллекции элементов, а циклы `for` — перебирать их.

### 1. Создание списка и добавление элементов:
```python
fruits = ["яблоко", "банан", "груша"]
fruits.append("апельсин")  # добавляет элемент в конец списка
print(len(fruits))         # длина списка: 4
```

### 2. Цикл `for`
Цикл `for` перебирает каждый элемент коллекции по очереди:

```python
numbers = [1, 2, 3, 4, 5]
total = 0
for num in numbers:
    total = total + num  # или total += num

print(f"Сумма: {total}")  # 15
```

### 3. Проверка четности числа:
Остаток от деления на 2 позволяет понять, четное число или нет:
```python
if num % 2 == 0:
    # Число четное
```

---

### Задание:
Напишите функцию `filter_evens_and_sum(numbers: list[int]) -> tuple[list[int], int]`:
1. Пройдитесь по списку `numbers` и отберите только **четные** числа в новый список `evens`.
2. Посчитайте сумму отобранных четных чисел `total_sum`. Если четных чисел нет, сумма равна `0`.
3. Верните кортеж из двух значений: `(evens, total_sum)`.
""",
            "task_description": "Реализуйте функцию `filter_evens_and_sum(numbers: list[int]) -> tuple[list[int], int]`, которая отбирает четные числа и находит их сумму.",
            "starter_code": """def filter_evens_and_sum(numbers: list[int]) -> tuple[list[int], int]:
    \"\"\"
    Отбирает четные числа из списка и вычисляет их сумму.
    Возвращает (список_четных, сумма).
    \"\"\"
    # TODO: Создайте пустой список evens = []
    # TODO: Пройдитесь циклом for num in numbers:
    # TODO: Если num % 2 == 0, добавьте в evens через .append(num)
    # TODO: Верните (evens, total_sum)
    pass
""",
            "hints": [
                {
                    "level": 1,
                    "title": "Инициализация",
                    "content": "Перед циклом создайте `evens = []` и переменную `total_sum = 0`."
                },
                {
                    "level": 2,
                    "title": "Тело цикла",
                    "content": "Внутри цикла: `if num % 2 == 0: evens.append(num); total_sum += num`."
                },
                {
                    "level": 3,
                    "title": "Возврат кортежа",
                    "content": "В конце функции верните оба значения через запятую: `return evens, total_sum`."
                }
            ],
            "solution": """def filter_evens_and_sum(numbers: list[int]) -> tuple[list[int], int]:
    \"\"\"
    Отбираем четные элементы и считаем их сумму.
    \"\"\"
    evens = []
    total_sum = 0
    for num in numbers:
        if num % 2 == 0:
            evens.append(num)
            total_sum += num
    return evens, total_sum
""",
            "test_suite_code": """
@pydeep_test("Смешанный список четных и нечетных")
def test_mixed():
    evens, s = filter_evens_and_sum([1, 2, 3, 4, 5, 6])
    assert evens == [2, 4, 6], f"Ожидались четные [2, 4, 6], получено: {evens}"
    assert s == 12, f"Ожидалась сумма 12, получено: {s}"
    return True

@pydeep_test("Только нечетные числа")
def test_only_odds():
    evens, s = filter_evens_and_sum([1, 3, 5, 7])
    assert evens == []
    assert s == 0
    return True

@pydeep_test("Пустой входной список")
def test_empty():
    evens, s = filter_evens_and_sum([])
    assert evens == []
    assert s == 0
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
user["job"] = "Python Developer"  # Добавление новой пары
```

### 2. Проверка наличия ключа:
```python
if "email" in user:
    print("Email найден")
else:
    print("Email отсутствует")
```

### 3. Подсчет частоты элементов:
Словари идеально подходят для подсчета статистики:

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
4. Возвращает словарь частот слов.
""",
            "task_description": "Реализуйте функцию `count_words(words: list[str]) -> dict[str, int]`, которая приводит слова к нижнему регистру и подсчитывает частоту каждого слова.",
            "starter_code": """def count_words(words: list[str]) -> dict[str, int]:
    \"\"\"
    Считает количество повторений каждого слова (в нижнем регистре).
    \"\"\"
    # TODO: Создайте пустой словарь counts = {}
    # TODO: Для каждого слова примените clean_word = word.lower()
    # TODO: Увеличьте счетчик в словаре
    # TODO: Верните counts
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
                    "content": "Проверьте: `if clean_word in counts: counts[clean_word] += 1` иначе `counts[clean_word] = 1`."
                },
                {
                    "level": 3,
                    "title": "Решение в одну строчку внутри цикла",
                    "content": "Можно использовать метод `.get(key, 0)`: `counts[clean_word] = counts.get(clean_word, 0) + 1`."
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
