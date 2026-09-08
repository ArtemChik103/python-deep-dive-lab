"""
Module 3: Advanced OOP, C3 MRO, Slots, and Dunder Protocols
"""

MODULE_3 = {
    "id": "module_3",
    "title": "Модуль 3: Глубокое ООП, Dunder-протоколы и MRO",
    "description": "Магические методы, линеаризация C3 MRO при множественном наследовании, кооперативный super() и __slots__ для экономии памяти.",
    "order": 3,
    "lessons": [
        {
            "id": "m3_l1_mro_cooperative_super",
            "title": "3.1. Линеаризация C3 MRO и кооперативный super()",
            "difficulty": "intermediate",
            "estimated_minutes": 30,
            "theory_md": """# Алгоритм C3 MRO и кооперативный `super()`

В Python множественное наследование разрешается по алгоритму **C3 Superclass Linearization**:
Порядок обхода классов доступен через `ClassName.__mro__` или `ClassName.mro()`.

### Принцип работы `super()`:
`super()` вызывает следующий метод **не у прямого родителя**, а у **следующего класса в MRO цепочке текущего экземпляра** (`self`)!

Для работы цепочки классов-миксинов (Mixins):
1. Каждый класс в цепочке должен передавать `*args, **kwargs` в `super().__init__(*args, **kwargs)`.
2. Базовый класс цепочки должен завершать вызовы (например, доходя до `object`).

```
      Base
     /    \\
  Logger  Validator
     \\    /
     Pipeline
```

### Задание:
Спроектируйте кооперативную цепочку классов:
1. `class JsonSerializableMixin`:
   - Метод `to_json() -> str`: сериализует словарь `self.__dict__` в JSON строку.
2. `class AuditedEntityMixin`:
   - В `__init__(*args, author: str = 'system', **kwargs)` сохраняет атрибуты `self.author = author` и вызывает `super()`.
   - Метод `get_audit_meta() -> dict`: возвращает `{"author": self.author, "class": self.__class__.__name__}`.
3. `class UserProfile(JsonSerializableMixin, AuditedEntityMixin)`:
   - В `__init__(username: str, email: str, **kwargs)` сохраняет `username` и `email` и передает остальное в `super().__init__(**kwargs)`.
""",
            "task_description": "Создайте кооперативные миксины и класс `UserProfile`, соблюдающие цепочку MRO и передачу kwargs в super().",
            "starter_code": """import json

class JsonSerializableMixin:
    def to_json(self) -> str:
        # TODO: Сериализуйте атрибуты экземпляра в JSON
        pass

class AuditedEntityMixin:
    def __init__(self, *args, author: str = "system", **kwargs):
        # TODO: Сохраните author и передайте super().__init__
        pass

    def get_audit_meta(self) -> dict:
        pass

class UserProfile(JsonSerializableMixin, AuditedEntityMixin):
    def __init__(self, username: str, email: str, **kwargs):
        # TODO: Инициализируйте поля профиля и передайте kwargs в super()
        pass
""",
            "hints": [
                {
                    "level": 1,
                    "title": "Концептуальная наводка",
                    "content": "Обратите внимание на вызовы super().__init__(**kwargs) во всех классах, чтобы kwargs доходили до AuditedEntityMixin независимо от порядка в MRO."
                },
                {
                    "level": 2,
                    "title": "Реализация to_json",
                    "content": "Для сериализации self.__dict__ используйте `json.dumps(self.__dict__, sort_keys=True)`."
                },
                {
                    "level": 3,
                    "title": "Каркас UserProfile",
                    "content": "```python\nclass UserProfile(JsonSerializableMixin, AuditedEntityMixin):\n    def __init__(self, username: str, email: str, **kwargs):\n        self.username = username\n        self.email = email\n        super().__init__(**kwargs)\n```"
                }
            ],
            "solution": """import json

class JsonSerializableMixin:
    \"\"\"Миксин для сериализации состояния экземпляра в JSON.\"\"\"
    def to_json(self) -> str:
        return json.dumps(self.__dict__, sort_keys=True)


class AuditedEntityMixin:
    \"\"\"Кооперативный миксин аудита, корректно передающий kwargs далее по MRO.\"\"\"
    def __init__(self, *args, author: str = "system", **kwargs):
        super().__init__(*args, **kwargs)
        self.author = author

    def get_audit_meta(self) -> dict:
        return {
            "author": self.author,
            "class": self.__class__.__name__
        }


class UserProfile(JsonSerializableMixin, AuditedEntityMixin):
    \"\"\"Конечный класс, объединяющий функционал обоих миксинов.\"\"\"
    def __init__(self, username: str, email: str, **kwargs):
        self.username = username
        self.email = email
        super().__init__(**kwargs)
""",
            "test_suite_code": """
@pydeep_test("Проверка MRO и инициализации полей")
def test_mro_cooperation():
    user = UserProfile(username="alex", email="alex@test.com", author="admin_root")
    assert user.username == "alex"
    assert user.email == "alex@test.com"
    assert user.author == "admin_root"
    assert user.get_audit_meta() == {"author": "admin_root", "class": "UserProfile"}
    return True

@pydeep_test("Проверка сериализации в JSON")
def test_json_serialization():
    import json
    user = UserProfile(username="dev_guru", email="guru@py.org")
    data = json.loads(user.to_json())
    assert data["username"] == "dev_guru"
    assert data["email"] == "guru@py.org"
    assert data["author"] == "system"
    return True
"""
        },
        {
            "id": "m3_l2_slots_memory_optimization",
            "title": "3.2. __slots__: устранение __dict__ и профилирование памяти",
            "difficulty": "advanced",
            "estimated_minutes": 25,
            "theory_md": """# Внутреннее устройство `__slots__`

По умолчанию у каждого экземпляра класса в Python есть словарь `__dict__`, где хранятся атрибуты.
Словарь `dict` имеет значительный оверхед по памяти (в среднем 100-200 байт на пустой словарь + хеш-таблица).

Когда создаются миллионы объектов (например, в высоконагруженных системах или графах данных):
`__slots__` указывает CPython выделить в структуре `PyObject` **фиксированный массив указателей** C-структуры вместо `__dict__`.

### Преимущества:
1. Экономия до 60-75% оперативной памяти на экземпляр.
2. Более быстрый доступ к атрибутам (через прямое смещение в структуре C, дескриптор `member_descriptor`).
3. Запрет случайного создания лишних атрибутов (защита от опечаток вроде `obj.usr_name = 'x'`).

### Правила наследования:
Если дочерний класс не определяет свой собственный `__slots__`, у него **снова появится `__dict__`**! Чтобы слоты работали в наследнике, нужно объявить `__slots__ = ()` или новые поля.

### Задание:
Реализуйте класс `Point3D`:
- Атрибуты: `x: float`, `y: float`, `z: float`.
- Должен использовать `__slots__ = ('x', 'y', 'z')` (не должен иметь `__dict__`!).
- Реализуйте метод `distance_to(other: 'Point3D') -> float`: евклидово расстояние $\\sqrt{(x_2-x_1)^2 + (y_2-y_1)^2 + (z_2-z_1)^2}$.
- Реализуйте метод `__repr__`: `Point3D(x=1.0, y=2.0, z=3.0)`.
- Реализуйте `__eq__` для сравнения координат.
""",
            "task_description": "Создайте класс `Point3D` с использованием `__slots__` и оптимизацией памяти.",
            "starter_code": """class Point3D:
    \"\"\"
    3D Точка со слотами __slots__ для максимальной экономии памяти.
    \"\"\"
    # TODO: Определите __slots__
    pass
""",
            "hints": [
                {
                    "level": 1,
                    "title": "Концептуальная наводка",
                    "content": "Объявите `__slots__ = ('x', 'y', 'z')` прямо в теле класса до методов."
                },
                {
                    "level": 2,
                    "title": "Вычисление расстояния",
                    "content": "Для вычисления расстояния используйте: math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2) или math.dist((self.x, self.y, self.z), (other.x, other.y, other.z))."
                },
                {
                    "level": 3,
                    "title": "Проверка отсутствия __dict__",
                    "content": "При правильном объявлении `__slots__` у экземпляра отсутствует атрибут `__dict__`: `hasattr(p, '__dict__')` вернет `False`."
                }
            ],
            "solution": """import math

class Point3D:
    \"\"\"
    Оптимизированная по памяти 3D-точка с фиксированными дескрипторами слотов.
    \"\"\"
    __slots__ = ('x', 'y', 'z')

    def __init__(self, x: float, y: float, z: float):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def distance_to(self, other: 'Point3D') -> float:
        return math.sqrt(
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2 +
            (self.z - other.z) ** 2
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point3D):
            return False
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)

    def __repr__(self) -> str:
        return f"Point3D(x={self.x}, y={self.y}, z={self.z})"
""",
            "test_suite_code": """
@pydeep_test("Проверка отсутствия __dict__ и запрета динамических атрибутов")
def test_slots_enforcement():
    p = Point3D(1.0, 2.0, 3.0)
    assert not hasattr(p, "__dict__"), "У класса со __slots__ не должно быть __dict__!"
    try:
        p.extra = 100
        assert False, "Присвоение незарегистрированного атрибута должно вызывать AttributeError"
    except AttributeError:
        pass
    return True

@pydeep_test("Проверка расчета расстояния")
def test_distance():
    p1 = Point3D(0.0, 0.0, 0.0)
    p2 = Point3D(3.0, 4.0, 0.0)
    assert p1.distance_to(p2) == 5.0
    return True
"""
        }
    ]
}
