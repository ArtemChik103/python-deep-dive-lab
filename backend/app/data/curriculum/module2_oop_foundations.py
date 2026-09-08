"""
Module 2: OOP Foundations
Classes, objects, __init__, self, encapsulation, @property, and __repr__.
Builds the essential foundation before advanced dunder protocols and hash contracts.
"""

MODULE_OOP_FOUNDATIONS = {
    "id": "module_oop_foundations",
    "title": "Модуль 2: Основы ООП (Классы и Объекты)",
    "description": "Понятие класса и экземпляра, конструктор __init__, ключевое слово self, инкапсуляция, свойства @property и метод __repr__.",
    "order": 2,
    "lessons": [
        {
            "id": "m2_f1_classes_init_self",
            "title": "2.1. Создание классов: __init__, self и методы",
            "difficulty": "beginner",
            "estimated_minutes": 15,
            "theory_md": """# Объектно-Ориентированное Программирование: Основы

ООП позволяет объединять **данные (состояние)** и **функции для работы с ними (поведение)** в единые сущности — **объекты**.

### 1. Класс и Экземпляр:
- **Класс (Class)** — это «чертеж» или шаблон (например, «Банковский счет»).
- **Экземпляр (Instance)** — это конкретный объект, созданный по этому чертежу (например, «счет Ивана с балансом 5000 руб.»).

### 2. Конструктор `__init__` и параметр `self`:
- Метод `__init__` вызывается автоматически в момент создания нового объекта.
- `self` — это ссылка на *текущий конкретный экземпляр* класса. Через `self.имя_поля` мы сохраняем атрибуты внутри объекта.

```python
class Dog:
    def __init__(self, name: str, breed: str):
        self.name = name      # атрибут экземпляра
        self.breed = breed
        self.tricks = []

    def learn_trick(self, trick: str) -> None:
        self.tricks.append(trick)
        print(f"{self.name} выучил трюк: {trick}")

# Создание экземпляра:
my_dog = Dog("Бобик", "Корги")
my_dog.learn_trick("сидеть")
```

---

### Задание:
Реализуйте класс `BankAccount`:
1. `__init__(self, owner: str, initial_balance: float = 0.0)`:
   - Сохраняет имя владельца в `self.owner`.
   - Если `initial_balance < 0`, вызывает `ValueError("Начальный баланс не может быть отрицательным")`.
   - Сохраняет баланс в `self.balance`.
   - Инициализирует пустой список истории транзакций `self.transactions = []`.
2. `deposit(self, amount: float) -> float`:
   - Если `amount <= 0`, вызывает `ValueError("Сумма пополнения должна быть положительной")`.
   - Увеличивает `self.balance` на `amount`.
   - Добавляет запись в `self.transactions`: `f"+{amount:.2f}"`.
   - Возвращает текущий баланс `self.balance`.
3. `withdraw(self, amount: float) -> float`:
   - Если `amount <= 0`, вызывает `ValueError("Сумма списания должна быть положительной")`.
   - Если `amount > self.balance`, вызывает `ValueError("Недостаточно средств")`.
   - Уменьшает `self.balance` на `amount`.
   - Добавляет запись в `self.transactions`: `f"-{amount:.2f}"`.
   - Возвращает текущий баланс `self.balance`.
""",
            "task_description": "Создайте класс `BankAccount` с методами deposit, withdraw и историей операций transactions.",
            "starter_code": """class BankAccount:
    \"\"\"
    Банковский счет с контролем баланса и историей операций.
    \"\"\"
    def __init__(self, owner: str, initial_balance: float = 0.0):
        # TODO: Проверьте initial_balance >= 0
        # TODO: Сохраните self.owner, self.balance, self.transactions = []
        pass

    def deposit(self, amount: float) -> float:
        # TODO: Проверьте amount > 0, пополните баланс, зафиксируйте транзакцию
        pass

    def withdraw(self, amount: float) -> float:
        # TODO: Проверьте amount > 0 и amount <= balance, спишите баланс, зафиксируйте транзакцию
        pass
""",
            "hints": [
                {
                    "level": 1,
                    "title": "Конструктор",
                    "content": "В `__init__`: если `initial_balance < 0: raise ValueError(...)`. Затем `self.owner = owner`, `self.balance = float(initial_balance)`, `self.transactions = []`."
                },
                {
                    "level": 2,
                    "title": "Проверки в методах",
                    "content": "В `withdraw`: сначала `if amount <= 0: raise ValueError(...)`, затем `if amount > self.balance: raise ValueError(...)`."
                },
                {
                    "level": 3,
                    "title": "История транзакций",
                    "content": "При deposit: `self.transactions.append(f'+{amount:.2f}')`. При withdraw: `self.transactions.append(f'-{amount:.2f}')`."
                }
            ],
            "solution": """class BankAccount:
    \"\"\"
    Эталонная реализация банковского счета с инкапсуляцией.
    \"\"\"
    def __init__(self, owner: str, initial_balance: float = 0.0):
        if initial_balance < 0:
            raise ValueError("Начальный баланс не может быть отрицательным")
        self.owner = owner
        self.balance = float(initial_balance)
        self.transactions: list[str] = []

    def deposit(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть положительной")
        self.balance += amount
        self.transactions.append(f"+{amount:.2f}")
        return self.balance

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Сумма списания должна быть положительной")
        if amount > self.balance:
            raise ValueError("Недостаточно средств")
        self.balance -= amount
        self.transactions.append(f"-{amount:.2f}")
        return self.balance
""",
            "test_suite_code": """
@pydeep_test("Успешное открытие счета и пополнение")
def test_account_lifecycle():
    acc = BankAccount("Алексей", 1000.0)
    assert acc.owner == "Алексей"
    assert acc.balance == 1000.0
    bal = acc.deposit(500.0)
    assert bal == 1500.0
    assert acc.balance == 1500.0
    assert acc.transactions == ["+500.00"]
    return True

@pydeep_test("Списание и проверка недостатка средств")
def test_withdraw_and_insufficient_funds():
    acc = BankAccount("Мария", 200.0)
    acc.withdraw(150.0)
    assert acc.balance == 50.0
    assert acc.transactions == ["-150.00"]
    
    # Попытка снять больше остатка
    try:
        acc.withdraw(100.0)
        assert False, "Ожидалось исключение ValueError при овердрафте"
    except ValueError:
        pass
    return True

@pydeep_test("Отрицательный начальный баланс")
def test_negative_initial():
    try:
        BankAccount("Тест", -50.0)
        assert False, "Ожидался ValueError"
    except ValueError:
        pass
    return True
"""
        },
        {
            "id": "m2_f2_properties_dunder_repr",
            "title": "2.2. Свойства @property и метод отображения __repr__",
            "difficulty": "beginner",
            "estimated_minutes": 15,
            "theory_md": """# Свойства `@property` и Магический метод `__repr__`

В Python принято избегать громоздких Java-подобных геттеров и сеттеров `get_balance()` / `set_balance()`. Вместо них используется элегантный декоратор `@property`.

### 1. Декоратор `@property`:
Позволяет обращаться к методу так, будто это обычный атрибут (без скобок `()`):

```python
class Circle:
    def __init__(self, radius: float):
        self.radius = radius

    @property
    def area(self) -> float:
        return 3.14159 * (self.radius ** 2)

c = Circle(5)
print(c.area)  # Обращение без вызова ()!
```

### 2. Сеттеры свойств `@name.setter`:
Позволяют валидировать новые значения при присваивании:
```python
class Product:
    def __init__(self, price: float):
        self._price = price

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, val: float):
        if val < 0:
            raise ValueError("Цена не может быть отрицательной")
        self._price = val
```

### 3. Метод `__repr__`:
Определяет строковое представление объекта для разработчика (при выводе в консоли или отладчике):
```python
def __repr__(self) -> str:
    return f"Circle(radius={self.radius})"
```

---

### Задание:
Реализуйте класс `Temperature`:
1. `__init__(self, celsius: float = 0.0)`:
   - Сохраняет значение температуры в градусах Цельсия в защищенное поле `self._celsius`.
2. Свойство `celsius`:
   - Геттер `@property def celsius(self) -> float`: возвращает текущую температуру в Цельсиях.
   - Сеттер `@celsius.setter def celsius(self, value: float)`: если `value < -273.15` (ниже абсолютного нуля), вызывает `ValueError("Температура ниже абсолютного нуля")`. Иначе сохраняет в `self._celsius`.
3. Свойство `fahrenheit`:
   - Геттер `@property def fahrenheit(self) -> float`: вычисляет и возвращает температуру в Фаренгейтах по формуле: `celsius * 9 / 5 + 32`.
   - Сеттер `@fahrenheit.setter def fahrenheit(self, value: float)`: переводит градусы Фаренгейта в Цельсии `(value - 32) * 5 / 9` и присваивает свойству `self.celsius` (что автоматически проверит абсолютный ноль!).
4. Метод `__repr__(self) -> str`:
   - Возвращает строку: `f"Temperature({self.celsius:.1f}°C)"`.
""",
            "task_description": "Создайте класс `Temperature` со свойствами celsius, fahrenheit, валидацией абсолютного нуля и методом __repr__.",
            "starter_code": """class Temperature:
    \"\"\"
    Температура с автоматической конвертацией Цельсий <-> Фаренгейт и защитой от абсолютного нуля.
    \"\"\"
    def __init__(self, celsius: float = 0.0):
        # TODO: Инициализируйте self.celsius (вызовет сеттер для проверки)
        pass

    # TODO: Реализуйте property celsius (getter + setter с проверкой < -273.15)
    # TODO: Реализуйте property fahrenheit (getter + setter)
    # TODO: Реализуйте __repr__
""",
            "hints": [
                {
                    "level": 1,
                    "title": "Хранение данных",
                    "content": "Внутри класса храните данные в приватном поле `self._celsius`. В конструкторе присвойте `self.celsius = celsius`."
                },
                {
                    "level": 2,
                    "title": "Формулы конвертации",
                    "content": "Фаренгейт: `self._celsius * 9 / 5 + 32`. Обратно из Фаренгейта: `(value - 32) * 5 / 9`."
                },
                {
                    "level": 3,
                    "title": "Структура сеттеров",
                    "content": "```python\n@celsius.setter\ndef celsius(self, val: float):\n    if val < -273.15:\n        raise ValueError(\"Ниже абсолютного нуля\")\n    self._celsius = float(val)\n```"
                }
            ],
            "solution": """class Temperature:
    \"\"\"
    Эталонная реализация класса температуры со свойствами.
    \"\"\"
    def __init__(self, celsius: float = 0.0):
        self._celsius = 0.0
        self.celsius = celsius

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < -273.15:
            raise ValueError("Температура ниже абсолютного нуля")
        self._celsius = float(value)

    @property
    def fahrenheit(self) -> float:
        return self._celsius * 9.0 / 5.0 + 32.0

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        celsius_val = (value - 32.0) * 5.0 / 9.0
        self.celsius = celsius_val

    def __repr__(self) -> str:
        return f"Temperature({self.celsius:.1f}°C)"
""",
            "test_suite_code": """
@pydeep_test("Конвертация 0°C в 32°F")
def test_zero_celsius():
    t = Temperature(0.0)
    assert t.celsius == 0.0
    assert t.fahrenheit == 32.0
    assert repr(t) == "Temperature(0.0°C)"
    return True

@pydeep_test("Изменение через fahrenheit сеттер")
def test_fahrenheit_setter():
    t = Temperature(0.0)
    t.fahrenheit = 212.0
    assert abs(t.celsius - 100.0) < 1e-4, f"Ожидалось 100°C, получено: {t.celsius}"
    assert repr(t) == "Temperature(100.0°C)"
    return True

@pydeep_test("Защита от температуры ниже абсолютного нуля")
def test_absolute_zero_protection():
    try:
        Temperature(-300.0)
        assert False, "Ожидалось исключение ValueError при температуре ниже -273.15°C"
    except ValueError:
        pass
    return True
"""
        }
    ]
}
