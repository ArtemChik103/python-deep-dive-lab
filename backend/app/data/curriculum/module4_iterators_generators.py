"""
Module 4: Iterators, Generators, and Stream Processing
The iterator protocol, lazy evaluation, yield from, and bidirectional coroutines.
"""

MODULE_4 = {
    "id": "module_4",
    "title": "Модуль 6: Итераторы, Генераторы и Потоковая обработка",
    "description": "Протокол итератора (__iter__ и __next__), генераторы с yield, делегирование yield from и корутины генераторов со связью через .send().",
    "order": 6,
    "lessons": [
        {
            "id": "m4_l1_custom_iterator_protocol",
            "title": "6.1. Протокол итератора: __iter__, __next__ и ленивый ChunkIterator",
            "difficulty": "intermediate",
            "estimated_minutes": 25,
            "theory_md": """# Протокол итератора (Iterator Protocol)

В Python итерируемый объект (`Iterable`) и сам итератор (`Iterator`) разделены:
1. **Iterable**: реализует метод `__iter__()`, возвращающий итератор.
2. **Iterator**: реализует `__iter__()` (возвращает `self`) и `__next__()` (возвращает следующий элемент или вызывает `StopIteration`).

### Зачем писать собственный итератор вместо list comprehension?
- Память: $O(1)$ по сравнению с $O(N)$ для списков.
- Ленивость: элементы генерируются по требованию.

### Задание:
Реализуйте класс `ChunkIterator(iterable, chunk_size: int)`:
- Принимает любой `iterable` (список, генератор, range) и размер пакета `chunk_size`.
- При каждой итерации возвращает список элементов длиной до `chunk_size`.
- Последний чанк может быть короче `chunk_size`.
- Реализуйте итератор **лениво**: не загружайте весь `iterable` в память сразу (`list(iterable)` запрещен, так как поток данных может быть бесконечным!).
""",
            "task_description": "Создайте ленивый разбивающий итератор `ChunkIterator` строго по протоколу `__iter__` и `__next__`.",
            "starter_code": """class ChunkIterator:
    \"\"\"
    Ленивый итератор, группирующий поток данных в пакеты (chunks) фиксированного размера.
    \"\"\"
    def __init__(self, iterable, chunk_size: int):
        # TODO: Сохраните итератор и размер чанка
        pass

    def __iter__(self):
        return self

    def __next__(self) -> list:
        # TODO: Соберите чанк размером до chunk_size или вызовите StopIteration
        pass
""",
            "hints": [
                {
                    "level": 1,
                    "title": "Концептуальная наводка",
                    "content": "Сохраните `self._it = iter(iterable)` в конструкторе. Это позволит обрабатывать как списки, так и генераторы."
                },
                {
                    "level": 2,
                    "title": "Сбор элементов чанка",
                    "content": "В `__next__` создайте пустой список `chunk = []`. В цикле от 0 до `chunk_size` вызывайте `next(self._it)`. Поймайте `StopIteration`, когда элементы закончатся."
                },
                {
                    "level": 3,
                    "title": "Завершение итератора",
                    "content": "Если `chunk` пуст и пойман `StopIteration`, нужно выбросить `StopIteration`. Если в `chunk` успели собраться элементы, верните `chunk`, а `StopIteration` сработает на следующем вызове."
                }
            ],
            "solution": """class ChunkIterator:
    \"\"\"
    Ленивый упаковщик потока данных с O(chunk_size) памяти.
    \"\"\"
    def __init__(self, iterable, chunk_size: int):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0")
        self._iterator = iter(iterable)
        self._chunk_size = chunk_size
        self._exhausted = False

    def __iter__(self):
        return self

    def __next__(self) -> list:
        if self._exhausted:
            raise StopIteration

        chunk = []
        for _ in range(self._chunk_size):
            try:
                chunk.append(next(self._iterator))
            except StopIteration:
                self._exhausted = True
                break

        if not chunk:
            raise StopIteration

        return chunk
""",
            "test_suite_code": """
@pydeep_test("Проверка разбиения на равные части")
def test_even_chunks():
    ci = ChunkIterator(range(6), 2)
    assert list(ci) == [[0, 1], [2, 3], [4, 5]]
    return True

@pydeep_test("Проверка последнего неполного чанка")
def test_odd_chunks():
    ci = ChunkIterator([1, 2, 3, 4, 5], 2)
    assert list(ci) == [[1, 2], [3, 4], [5]]
    return True

@pydeep_test("Ленивая работа с генератором")
def test_lazy_stream():
    def infinite_counter():
        n = 0
        while True:
            yield n
            n += 1
    ci = ChunkIterator(infinite_counter(), 3)
    chunk1 = next(ci)
    chunk2 = next(ci)
    assert chunk1 == [0, 1, 2]
    assert chunk2 == [3, 4, 5]
    return True
"""
        },
        {
            "id": "m4_l2_yield_from_coroutines",
            "title": "6.2. yield from и двусторонняя связь через .send()",
            "difficulty": "advanced",
            "estimated_minutes": 30,
            "theory_md": """# Конструкция `yield from` и корутины генераторов

Генераторы в Python — это не просто итераторы, а полноценные симметричные корутины:
1. `yield` может не только отдавать значение наружу, но и **принимать** значение извне через вызов генератора `.send(value)`!
2. `yield from subgen`:
   - Автоматически делегирует итерацию дочернему генератору.
   - Прозрачно перенаправляет вызовы `.send()` и `.throw()` прямо в подгенератор.
   - При завершении подгенератора возвращает значение из его `return result`!

```python
def sub():
    val = yield "start"
    return f"Done with {val}"

def delegator():
    res = yield from sub()
    yield f"Result: {res}"
```

### Задание:
Реализуйте функцию-генератор `running_average_coroutine()`:
- При запуске ожидает значений через `.send(number: float)`.
- На каждом шаге `yield` отдает текущее скользящее среднее `float` (округленное до 2 знаков).
- Если передано `None` или генератор закрыт, возвращает кортеж `(count, final_average)` через `return`.
""",
            "task_description": "Создайте корутину генератора `running_average_coroutine`, принимающую значения через `.send()`.",
            "starter_code": """def running_average_coroutine():
    \"\"\"
    Генераторная корутина: принимает числа через .send(val) и возвращает текущее среднее.
    \"\"\"
    # TODO: Реализуйте цикл yield с приемом значений
    pass
""",
            "hints": [
                {
                    "level": 1,
                    "title": "Концептуальная наводка",
                    "content": "Используйте конструкцию `received = yield current_avg`. Помните, что перед первым `.send(val)` генератор нужно инициализировать (`next(gen)` или `.send(None)`)."
                },
                {
                    "level": 2,
                    "title": "Подсчет скользящего среднего",
                    "content": "Храните `total = 0.0` и `count = 0`. В цикле обновляйте: `count += 1; total += val; avg = round(total / count, 2); val = yield avg`."
                },
                {
                    "level": 3,
                    "title": "Возврат значения через return",
                    "content": "Если `val is None`: прервите цикл и верните `return (count, round(total / count, 2) if count else 0.0)`."
                }
            ],
            "solution": """def running_average_coroutine():
    \"\"\"
    Двусторонняя генераторная корутина.
    \"\"\"
    total = 0.0
    count = 0
    val = yield None

    while val is not None:
        count += 1
        total += float(val)
        current_avg = round(total / count, 2)
        val = yield current_avg

    final_avg = round(total / count, 2) if count > 0 else 0.0
    return (count, final_avg)
""",
            "test_suite_code": """
@pydeep_test("Проверка отправки значений через .send()")
def test_send_flow():
    gen = running_average_coroutine()
    next(gen)  # Инициализация (prime)
    assert gen.send(10) == 10.0
    assert gen.send(20) == 15.0
    assert gen.send(30) == 20.0
    return True

@pydeep_test("Проверка возврата финального значения в StopIteration")
def test_return_value():
    gen = running_average_coroutine()
    next(gen)
    gen.send(10)
    gen.send(30)
    try:
        gen.send(None)
        assert False, "Должен быть StopIteration при завершении"
    except StopIteration as si:
        assert si.value == (2, 20.0)
    return True
"""
        }
    ]
}
