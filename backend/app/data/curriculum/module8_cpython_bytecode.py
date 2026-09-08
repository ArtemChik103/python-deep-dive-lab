"""
Module 8: CPython Internals, Bytecode, Garbage Collection, and Weak References
"""

MODULE_8 = {
    "id": "module_8",
    "title": "Модуль 10: Внутренности CPython, Байткод и Управление Памятью",
    "description": "Стековая машина CPython, опкоды dis, счетчик ссылок (refcount), циклический сборщик мусора gc и слабые ссылки weakref.",
    "order": 10,
    "lessons": [
        {
            "id": "m8_l1_cpython_bytecode_dis",
            "title": "10.1. Дизассемблирование байткода CPython: модуль dis",
            "difficulty": "expert",
            "estimated_minutes": 35,
            "theory_md": """# Стековая виртуальная машина CPython и байткод

CPython — это **стековая машина**. Исходный код Python сначала компилируется в AST, а затем в последовательность инструкций байткода:
- `LOAD_FAST / STORE_FAST`: быстрая работа с локальными переменными (индексация по C-массиву).
- `LOAD_GLOBAL / STORE_GLOBAL`: медленный поиск по словарям `globals()` и `builtins`.
- `BINARY_OP`: выполнение арифметических или побитовых операций со стеком.
- `RETURN_VALUE`: снятие вершины стека и возврат значения.

Модуль `dis` позволяет анализировать скомпилированный код:
```python
import dis
instructions = list(dis.get_instructions(my_function))
for ins in instructions:
    print(ins.opname, ins.argval)
```

### Задание:
Напишите функцию `analyze_function_bytecode(func) -> dict`:
- Использует `dis.get_instructions(func)` для анализа переданной функции.
- Возвращает статистику в виде словаря:
  - `"total_instructions": int` — общее число опкодов.
  - `"opcode_counts": dict[str, int]` — частота каждого опкода (например, `{"LOAD_FAST": 4, "RETURN_VALUE": 1}`).
  - `"uses_global_lookup": bool` — содержит ли функция инструкции `LOAD_GLOBAL` или `STORE_GLOBAL`.
  - `"local_variables": list[str]` — отсортированный список всех уникальных имен локальных переменных, к которым обращаются через `LOAD_FAST` / `STORE_FAST`.
""",
            "task_description": "Создайте анализатор байткода функции `analyze_function_bytecode` с использованием модуля `dis`.",
            "starter_code": """import dis

def analyze_function_bytecode(func) -> dict:
    \"\"\"
    Анализирует байткод функции и возвращает статистику инструкций.
    \"\"\"
    # TODO: Получите инструкции через dis.get_instructions(func) и соберите статистику
    pass
""",
            "hints": [
                {
                    "level": 1,
                    "title": "Концептуальная наводка",
                    "content": "Используйте `dis.get_instructions(func)`. У каждой инструкции есть атрибуты: `ins.opname`, `ins.argval`."
                },
                {
                    "level": 2,
                    "title": "Фильтрация локальных переменных",
                    "content": "Если `ins.opname in ('LOAD_FAST', 'STORE_FAST')`, добавляйте `ins.argval` в множество локальных переменных: `locals_set.add(str(ins.argval))`."
                },
                {
                    "level": 3,
                    "title": "Проверка глобального доступа",
                    "content": "Проверьте: `uses_global_lookup = any('GLOBAL' in ins.opname for ins in instructions)`."
                }
            ],
            "solution": """import dis
from collections import Counter

def analyze_function_bytecode(func) -> dict:
    \"\"\"
    Эталонный инспектор байткода CPython.
    \"\"\"
    instructions = list(dis.get_instructions(func))
    total = len(instructions)
    counts = Counter(ins.opname for ins in instructions)
    
    uses_globals = any(
        ins.opname in ("LOAD_GLOBAL", "STORE_GLOBAL")
        for ins in instructions
    )
    
    local_vars = set()
    for ins in instructions:
        if ins.opname in ("LOAD_FAST", "STORE_FAST") and ins.argval is not None:
            local_vars.add(str(ins.argval))

    return {
        "total_instructions": total,
        "opcode_counts": dict(counts),
        "uses_global_lookup": uses_globals,
        "local_variables": sorted(local_vars)
    }
""",
            "test_suite_code": """
def sample_pure_func(a, b):
    temp = a + b
    return temp * 2

def sample_global_func(x):
    return len(str(x))

@pydeep_test("Анализ чистой локальной функции")
def test_pure_bytecode():
    report = analyze_function_bytecode(sample_pure_func)
    assert report["total_instructions"] > 0
    assert "RETURN_VALUE" in report["opcode_counts"]
    assert report["uses_global_lookup"] is False
    assert report["local_variables"] == ["a", "b", "temp"]
    return True

@pydeep_test("Обнаружение обращений к глобалам")
def test_global_bytecode():
    report = analyze_function_bytecode(sample_global_func)
    assert report["uses_global_lookup"] is True
    return True
"""
        },
        {
            "id": "m8_l2_garbage_collection_weakref",
            "title": "10.2. Reference Counting, циклический GC и weakref кэш",
            "difficulty": "expert",
            "estimated_minutes": 35,
            "theory_md": """# Управление памятью: Refcount, Cyclic GC и `weakref`

В CPython управление памятью базируется на двух китах:
1. **Reference Counting (подсчет ссылок)**: каждый `PyObject` содержит счетчик `ob_refcnt`. Когда счетчик падает до 0, память освобождается **немедленно**.
2. **Cyclic Garbage Collector (gc)**: циклические ссылки (когда объект А ссылается на Б, а Б ссылается на А) никогда не достигнут 0 по refcount. Для них работает трехпоколенный циклический сборщик мусора (Generation 0, 1, 2).

### Проблема кэширования:
Обычный словарь `cache[key] = heavy_object` удерживает жесткую ссылку (`strong reference`), из-за чего объект никогда не удалится из памяти, вызывая утечку памяти (Memory Leak).

`weakref.WeakValueDictionary` хранит **слабые ссылки**:
Если на объект больше нет обычных внешних ссылок, сборщик мусора CPython автоматически удаляет объект, а запись из словаря `WeakValueDictionary` исчезает сама!

### Задание:
Реализуйте класс `AutoCleaningObjectRegistry`:
- Использует `weakref.WeakValueDictionary` для регистрации объектов по уникальному ключу `str`.
- Метод `register(key: str, obj: object) -> None`: регистрирует объект.
- Метод `get(key: str) -> object | None`: возвращает объект или `None`, если он был собран сборщиком мусора.
- Метод `active_count() -> int`: возвращает текущее число живых зарегистрированных объектов.
- Метод `contains(key: str) -> bool`: проверяет наличие живого ключа.
""",
            "task_description": "Создайте самоочищающийся реестр объектов на базе `weakref.WeakValueDictionary`.",
            "starter_code": """import weakref

class AutoCleaningObjectRegistry:
    \"\"\"
    Реестр объектов на слабых ссылках, автоматически очищающий удаленные объекты.
    \"\"\"
    def __init__(self):
        # TODO: Инициализируйте WeakValueDictionary
        pass

    def register(self, key: str, obj: object) -> None:
        pass

    def get(self, key: str):
        pass

    def active_count(self) -> int:
        pass

    def contains(self, key: str) -> bool:
        pass
""",
            "hints": [
                {
                    "level": 1,
                    "title": "Концептуальная наводка",
                    "content": "Инициализируйте `self._storage = weakref.WeakValueDictionary()`."
                },
                {
                    "level": 2,
                    "title": "Особенность слабых ссылок",
                    "content": "Помните: слабые ссылки можно создавать на пользовательские классы. Примитивные типы вроде `str` или `int` в CPython не поддерживают weakref."
                },
                {
                    "level": 3,
                    "title": "Методы работы",
                    "content": "```python\ndef register(self, key: str, obj: object):\n    self._storage[key] = obj\ndef active_count(self) -> int:\n    return len(self._storage)\n```"
                }
            ],
            "solution": """import weakref

class AutoCleaningObjectRegistry:
    \"\"\"
    Эталонный реестр с автоматической очисткой при сборке мусора.
    \"\"\"
    def __init__(self):
        self._storage: weakref.WeakValueDictionary = weakref.WeakValueDictionary()

    def register(self, key: str, obj: object) -> None:
        self._storage[key] = obj

    def get(self, key: str):
        return self._storage.get(key, None)

    def active_count(self) -> int:
        return len(self._storage)

    def contains(self, key: str) -> bool:
        return key in self._storage
""",
            "test_suite_code": """
class HeavyResource:
    def __init__(self, name):
        self.name = name

@pydeep_test("Автоматическое удаление объекта из реестра при удалении последней ссылки")
def test_weakref_eviction():
    import gc
    reg = AutoCleaningObjectRegistry()
    
    res1 = HeavyResource("DB_Connection")
    reg.register("conn_1", res1)
    
    assert reg.active_count() == 1
    assert reg.contains("conn_1") is True
    assert reg.get("conn_1") is res1
    
    # Удаляем единственную сильную ссылку
    del res1
    gc.collect()
    
    # Объект должен автоматически исчезнуть из реестра
    assert reg.active_count() == 0
    assert reg.contains("conn_1") is False
    assert reg.get("conn_1") is None
    return True
"""
        }
    ]
}
