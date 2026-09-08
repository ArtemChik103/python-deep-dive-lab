"""
Module 9: Modern Static Typing, Protocols, and Generics
"""

MODULE_9 = {
    "id": "module_9",
    "title": "Модуль 11: Статическая Типизация, Protocol и Generics",
    "description": "Структурная подтипизация с typing.Protocol (статический duck-typing), обобщенные типы Generic[T], TypeVar и монада Result[T, E].",
    "order": 11,
    "lessons": [
        {
            "id": "m9_l1_structural_typing_protocol",
            "title": "11.1. Структурная подтипизация: Protocol и runtime_checkable",
            "difficulty": "advanced",
            "estimated_minutes": 25,
            "theory_md": """# Структурная подтипизация: `typing.Protocol`

Python традиционно использует **утиную типизацию (Duck Typing)**: «Если это крякает как утка — это утка».
Но как совместить это со статической проверкой типов (Mypy, Pyright)?

В PEP 544 представлен `typing.Protocol`:
- Классы **НЕ обязаны наследоваться** от протокола явно.
- Любой класс, у которого совпадают методы и сигнатуры, считается валидным подтипом!
- Декоратор `@runtime_checkable` позволяет использовать `isinstance(obj, MyProtocol)` в рантайме.

### Задание:
1. Создайте протокол `Renderable(Protocol)` с декоратором `@runtime_checkable`:
   - Метод `render(self) -> str`.
2. Напишите функцию `render_pipeline(items: list) -> list[str]`:
   - Принимает список любых объектов.
   - Фильтрует только те объекты, которые удовлетворяют протоколу `Renderable` (`isinstance(item, Renderable)`).
   - Вызывает `.render()` для каждого подходящего объекта и возвращает список строк.
""",
            "task_description": "Создайте проверяемый в рантайме протокол `Renderable` и пайплайн фильтрации `render_pipeline`.",
            "starter_code": """from typing import Protocol, runtime_checkable

# TODO: Объявите протокол Renderable с методом render(self) -> str

def render_pipeline(items: list) -> list[str]:
    \"\"\"
    Фильтрует объекты по соответствию протоколу Renderable и возвращает результаты render().
    \"\"\"
    # TODO: Реализуйте функцию
    pass
""",
            "hints": [
                {
                    "level": 1,
                    "title": "Концептуальная наводка",
                    "content": "Используйте `@runtime_checkable` прямо над классом `class Renderable(Protocol): def render(self) -> str: ...`."
                },
                {
                    "level": 2,
                    "title": "Фильтрация объектов",
                    "content": "Пройдитесь по элементам: `[item.render() for item in items if isinstance(item, Renderable)]`."
                },
                {
                    "level": 3,
                    "title": "Готовый код протокола",
                    "content": "```python\n@runtime_checkable\nclass Renderable(Protocol):\n    def render(self) -> str:\n        ...\n```"
                }
            ],
            "solution": """from typing import Protocol, runtime_checkable

@runtime_checkable
class Renderable(Protocol):
    \"\"\"Протокол для объектов, умеющих рендериться в текстовое представление.\"\"\"
    def render(self) -> str:
        ...


def render_pipeline(items: list) -> list[str]:
    \"\"\"
    Фильтрация и вызов render() для всех объектов, поддерживающих протокол.
    \"\"\"
    return [item.render() for item in items if isinstance(item, Renderable)]
""",
            "test_suite_code": """
class MarkdownCard:
    def __init__(self, title):
        self.title = title
    def render(self) -> str:
        return f"# {self.title}"

class JsonDoc:
    def render(self) -> str:
        return "{'status': 'ok'}"

class NonRenderable:
    def execute(self):
        return True

@pydeep_test("Проверка структурного совпадения без наследования")
def test_structural_matching():
    card = MarkdownCard("Architecture")
    doc = JsonDoc()
    non_item = NonRenderable()
    
    assert isinstance(card, Renderable), "Класс без явного наследования должен удовлетворять протоколу"
    assert isinstance(doc, Renderable)
    assert not isinstance(non_item, Renderable)
    
    rendered = render_pipeline([card, non_item, doc, "just string"])
    assert rendered == ["# Architecture", "{'status': 'ok'}"]
    return True
"""
        },
        {
            "id": "m9_l2_generic_result_monad",
            "title": "11.2. Дженерики и Монада Result[T, E] для безопасной обработки ошибок",
            "difficulty": "advanced",
            "estimated_minutes": 30,
            "theory_md": """# Дженерики (Generics) и паттерн Result[T, E]

Исключения в Python удобны, но при обработке распределенных конвейеров данных они приводят к скрытым багам, если вызывающий код забыл обернуть вызов в `try-except`.

Паттерн `Result[T, E]` (пришедший из функционального программирования и Rust):
- Значение может быть либо `Ok(value: T)`, либо `Err(error: E)`.
- Позволяет строить цепочки преобразований через метод `.map(fn)`.

```python
T = TypeVar('T')
E = TypeVar('E')

class Result(Generic[T, E]):
    ...
```

### Задание:
Реализуйте обобщенные классы:
1. `class Result(Generic[T, E])`:
   - `is_ok: bool`
   - `is_err: bool`
   - Метод `map(self, fn)`: если `is_ok`, возвращает новый `Ok(fn(self.value))`, иначе возвращает текущий `self` без изменений.
   - Метод `unwrap(self)`: если `is_ok`, возвращает `self.value`, иначе выбрасывает `RuntimeError(str(self.error))`.
2. `class Ok(Result[T, Any])` и `class Err(Result[Any, E])`.
""",
            "task_description": "Создайте дженерик-контейнер `Result[T, E]` с подклассами `Ok` и `Err`.",
            "starter_code": """from typing import Generic, TypeVar, Any

T = TypeVar("T")
E = TypeVar("E")
U = TypeVar("U")

class Result(Generic[T, E]):
    # TODO: Определите базовый класс Result
    pass

class Ok(Result[T, Any]):
    # TODO: Реализуйте Ok
    pass

class Err(Result[Any, E]):
    # TODO: Реализуйте Err
    pass
""",
            "hints": [
                {
                    "level": 1,
                    "title": "Концептуальная наводка",
                    "content": "В классе Ok определите свойства `is_ok = True` и `is_err = False`. В Err соответственно наоборот."
                },
                {
                    "level": 2,
                    "title": "Реализация map",
                    "content": "В Ok: `def map(self, fn): return Ok(fn(self.value))`. В Err: `def map(self, fn): return self`."
                },
                {
                    "level": 3,
                    "title": "Реализация unwrap",
                    "content": "В Ok: `def unwrap(self): return self.value`. В Err: `def unwrap(self): raise RuntimeError(str(self.error))`."
                }
            ],
            "solution": """from typing import Generic, TypeVar, Any

T = TypeVar("T")
E = TypeVar("E")
U = TypeVar("U")

class Result(Generic[T, E]):
    is_ok: bool
    is_err: bool

    def map(self, fn):
        raise NotImplementedError

    def unwrap(self) -> T:
        raise NotImplementedError


class Ok(Result[T, Any]):
    is_ok = True
    is_err = False

    def __init__(self, value: T):
        self.value = value

    def map(self, fn) -> 'Ok':
        return Ok(fn(self.value))

    def unwrap(self) -> T:
        return self.value

    def __repr__(self) -> str:
        return f"Ok({self.value!r})"


class Err(Result[Any, E]):
    is_ok = False
    is_err = True

    def __init__(self, error: E):
        self.error = error

    def map(self, fn) -> 'Err':
        return self

    def unwrap(self):
        raise RuntimeError(str(self.error))

    def __repr__(self) -> str:
        return f"Err({self.error!r})"
""",
            "test_suite_code": """
@pydeep_test("Цепочка преобразований map для Ok")
def test_result_ok():
    res = Ok(10).map(lambda x: x * 2).map(lambda x: f"Score: {x}")
    assert res.is_ok is True
    assert res.is_err is False
    assert res.unwrap() == "Score: 20"
    return True

@pydeep_test("Пропуск map для Err и исключение при unwrap")
def test_result_err():
    res = Err("Database timeout").map(lambda x: x * 2)
    assert res.is_ok is False
    assert res.is_err is True
    try:
        res.unwrap()
        assert False, "unwrap() на Err должен вызывать RuntimeError"
    except RuntimeError as e:
        assert "Database timeout" in str(e)
    return True
"""
        }
    ]
}
