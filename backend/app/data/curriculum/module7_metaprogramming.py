"""
Module 7: Metaprogramming, Descriptors, and Metaclasses
"""

MODULE_7 = {
    "id": "module_7",
    "title": "Модуль 7: Метапрограммирование, Дескрипторы и Метаклассы",
    "description": "Протокол дескрипторов (__get__, __set__, __set_name__), разница между Data и Non-Data дескрипторами, магия метаклассов и __init_subclass__.",
    "order": 7,
    "lessons": [
        {
            "id": "m7_l1_descriptors_typed_field",
            "title": "7.1. Протокол дескрипторов: создание валидатора полей TypedField",
            "difficulty": "expert",
            "estimated_minutes": 35,
            "theory_md": """# Протокол дескрипторов в Python

Дескриптор — это объект с любым из методов:
- `__get__(self, instance, owner=None)`
- `__set__(self, instance, value)`
- `__delete__(self, instance)`
- `__set_name__(self, owner, name)` (добавлен в Python 3.6 для автоматического получения имени атрибута!)

### Data Descriptors vs Non-Data Descriptors:
- **Data descriptor**: реализует `__set__` или `__delete__`. Имеет наивысший приоритет при поиске атрибута: **всегда перекрывает словарь экземпляра `instance.__dict__`**!
- **Non-data descriptor**: реализует только `__get__` (например, обычный метод или `@classmethod`). Словарь `instance.__dict__` имеет приоритет над ним.

### Задание:
Реализуйте дескриптор данных `TypedField(expected_type, min_val=None, max_val=None)`:
- Использует `__set_name__(self, owner, name)` для автоматического сохранения имени поля в приватный слот экземпляра (например, `f"_{name}"`).
- В `__set__(self, instance, value)`:
  - Проверяет, что `isinstance(value, expected_type)`. Если нет — выбрасывает `TypeError`.
  - Если задан `min_val` и `value < min_val` — выбрасывает `ValueError`.
  - Если задан `max_val` и `value > max_val` — выбрасывает `ValueError`.
  - Сохраняет проверенное значение в словарь экземпляра `instance.__dict__`.
- В `__get__(self, instance, owner=None)`:
  - Если вызван от класса (`instance is None`) — возвращает сам объект дескриптора (`self`).
  - Если от экземпляра — возвращает сохраненное значение или `None`, если значение еще не задавалось.
""",
            "task_description": "Создайте валидирующий дескриптор данных `TypedField` с автоматической привязкой имени через `__set_name__`.",
            "starter_code": """class TypedField:
    \"\"\"
    Строго типизированный дескриптор поля с валидацией границ значений.
    \"\"\"
    def __init__(self, expected_type, min_val=None, max_val=None):
        # TODO: Инициализация параметров валидации
        pass

    def __set_name__(self, owner, name):
        # TODO: Сохраните имя атрибута
        pass

    def __get__(self, instance, owner=None):
        pass

    def __set__(self, instance, value):
        pass
""",
            "hints": [
                {
                    "level": 1,
                    "title": "Концептуальная наводка",
                    "content": "В методе `__set_name__(self, owner, name)` сохраните `self.storage_name = f'_{name}'` или `self.name = name`."
                },
                {
                    "level": 2,
                    "title": "Доступ через instance.__dict__",
                    "content": "Чтобы избежать рекурсии при присвоении, сохраняйте значение прямо в `instance.__dict__[self.storage_name] = value`."
                },
                {
                    "level": 3,
                    "title": "Обработка доступа от класса",
                    "content": "```python\ndef __get__(self, instance, owner=None):\n    if instance is None:\n        return self\n    return instance.__dict__.get(self.storage_name, None)\n```"
                }
            ],
            "solution": """class TypedField:
    \"\"\"
    Эталонный Data-дескриптор с валидацией типов и диапазонов.
    \"\"\"
    def __init__(self, expected_type, min_val=None, max_val=None):
        self.expected_type = expected_type
        self.min_val = min_val
        self.max_val = max_val
        self.name = None
        self.storage_name = None

    def __set_name__(self, owner, name):
        self.name = name
        self.storage_name = f"_{name}"

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return instance.__dict__.get(self.storage_name, None)

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"Field '{self.name}' must be of type {self.expected_type.__name__}, got {type(value).__name__}"
            )
        if self.min_val is not None and value < self.min_val:
            raise ValueError(f"Field '{self.name}' value {value} is below minimum {self.min_val}")
        if self.max_val is not None and value > self.max_val:
            raise ValueError(f"Field '{self.name}' value {value} exceeds maximum {self.max_val}")
        
        instance.__dict__[self.storage_name] = value
""",
            "test_suite_code": """
class InventoryItem:
    name = TypedField(str)
    quantity = TypedField(int, min_val=0, max_val=1000)
    price = TypedField((int, float), min_val=0.01)

@pydeep_test("Успешное присвоение корректных значений")
def test_valid_assignment():
    item = InventoryItem()
    item.name = "Laptop"
    item.quantity = 15
    item.price = 999.99
    assert item.name == "Laptop"
    assert item.quantity == 15
    assert item.price == 999.99
    return True

@pydeep_test("Проверка ошибки типа TypeError")
def test_invalid_type():
    item = InventoryItem()
    try:
        item.name = 12345
        assert False, "Должна быть ошибка TypeError"
    except TypeError:
        pass
    return True

@pydeep_test("Проверка валидации минимального значения")
def test_min_boundary():
    item = InventoryItem()
    try:
        item.quantity = -1
        assert False, "Должна быть ошибка ValueError для отрицательного количества"
    except ValueError:
        pass
    return True
"""
        },
        {
            "id": "m7_l2_init_subclass_plugin_registry",
            "title": "7.2. Авторегистрация через __init_subclass__ и метапрограммирование",
            "difficulty": "expert",
            "estimated_minutes": 30,
            "theory_md": """# Современное метапрограммирование: `__init_subclass__`

До появления PEP 487 в Python 3.6 для автоматической регистрации классов или модификации атрибутов при наследовании приходилось писать тяжеловесные метаклассы (`class Meta(type): ...`).

`__init_subclass__(cls, **kwargs)` вызывается автоматически каждый раз, когда от класса создается наследник:
- Работает чисто и декларативно.
- Может принимать именованные параметры прямо из определения класса: `class Child(Base, register_name="special"):`.
- Позволяет строить масштабируемые системы плагинов, RPC-хендлеров и парсеров команд.

### Задание:
Реализуйте базовый класс командного процессора `BaseCommand`:
- Имеет атрибут класса `registry = {}` (словарь зарегистрированных команд: `{command_name: command_class}`).
- Метод класса `__init_subclass__(cls, command_code: str = None, **kwargs)`:
  - Если `command_code` передан, регистрирует класс в `BaseCommand.registry` под этим именем.
  - Если класс с таким `command_code` уже есть в реестре, выбрасывает `ValueError("Duplicate command")`.
  - Требует обязательного наличия метода `execute(self, payload: dict) -> dict` у наследника; если метода нет — выбрасывает `TypeError("Missing execute method")`.
- Метод класса `dispatch(command_code: str, payload: dict) -> dict`:
  - Находит зарегистрированный класс, создает его экземпляр и вызывает `.execute(payload)`.
  - Если команда не найдена — выбрасывает `KeyError("Unknown command")`.
""",
            "task_description": "Создайте расширяемый реестр плагинов на базе `__init_subclass__` с валидацией интерфейса.",
            "starter_code": """class BaseCommand:
    \"\"\"
    Базовый класс с авторегистрацией дочерних команд через __init_subclass__.
    \"\"\"
    registry = {}

    # TODO: Реализуйте __init_subclass__ и dispatch
""",
            "hints": [
                {
                    "level": 1,
                    "title": "Концептуальная наводка",
                    "content": "В `__init_subclass__(cls, command_code=None, **kwargs)` не забудьте вызвать `super().__init_subclass__(**kwargs)`."
                },
                {
                    "level": 2,
                    "title": "Валидация интерфейса",
                    "content": "Проверьте: `if 'execute' not in cls.__dict__ and not hasattr(cls, 'execute'): raise TypeError(...)`."
                },
                {
                    "level": 3,
                    "title": "Реализация dispatch",
                    "content": "```python\n@classmethod\ndef dispatch(cls, command_code: str, payload: dict) -> dict:\n    cmd_class = cls.registry.get(command_code)\n    if not cmd_class:\n        raise KeyError('Unknown command')\n    return cmd_class().execute(payload)\n```"
                }
            ],
            "solution": """class BaseCommand:
    \"\"\"
    Базовый фреймворк команд с реестром на базе __init_subclass__.
    \"\"\"
    registry = {}

    def __init_subclass__(cls, command_code: str = None, **kwargs):
        super().__init_subclass__(**kwargs)
        if command_code is not None:
            if command_code in BaseCommand.registry:
                raise ValueError(f"Duplicate command code '{command_code}'")
            if not hasattr(cls, "execute") or not callable(getattr(cls, "execute")):
                raise TypeError(f"Class '{cls.__name__}' must implement callable 'execute(self, payload)'")
            BaseCommand.registry[command_code] = cls

    @classmethod
    def dispatch(cls, command_code: str, payload: dict) -> dict:
        cmd_cls = BaseCommand.registry.get(command_code)
        if not cmd_cls:
            raise KeyError(f"Unknown command '{command_code}'")
        instance = cmd_cls()
        return instance.execute(payload)
""",
            "test_suite_code": """
# Регистрация тестовых команд
class PingCommand(BaseCommand, command_code="ping"):
    def execute(self, payload: dict) -> dict:
        return {"response": "pong", "echo": payload.get("data")}

class EchoCommand(BaseCommand, command_code="echo"):
    def execute(self, payload: dict) -> dict:
        return {"echoed": payload.get("msg", "").upper()}

@pydeep_test("Автоматическая регистрация и диспетчеризация")
def test_dispatch():
    res1 = BaseCommand.dispatch("ping", {"data": 123})
    assert res1 == {"response": "pong", "echo": 123}
    
    res2 = BaseCommand.dispatch("echo", {"msg": "hello"})
    assert res2 == {"echoed": "HELLO"}
    return True

@pydeep_test("Запрет дубликатов кодов команд")
def test_duplicate_code():
    try:
        class DupCommand(BaseCommand, command_code="ping"):
            def execute(self, payload): pass
        assert False, "Должна быть ошибка ValueError из-за дубликата"
    except ValueError:
        pass
    return True
"""
        }
    ]
}
