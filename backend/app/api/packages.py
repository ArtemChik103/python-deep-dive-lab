from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.venv_manager import (
    install_package,
    list_installed_packages,
    uninstall_package,
)

router = APIRouter(prefix="/packages", tags=["packages"])

POPULAR_PACKAGES = [
    {
        "name": "numpy",
        "description": "Быстрые n-мерные массивы, векторные вычисления и линейная алгебра.",
        "category": "Data & Math",
        "docs_url": "https://numpy.org"
    },
    {
        "name": "pandas",
        "description": "Мощные структуры данных DataFrame для анализа и обработки таблиц.",
        "category": "Data & Math",
        "docs_url": "https://pandas.pydata.org"
    },
    {
        "name": "matplotlib",
        "description": "Построение графиков, диаграмм и визуализация данных (авто-рендер в UI!).",
        "category": "Visualization",
        "docs_url": "https://matplotlib.org"
    },
    {
        "name": "rich",
        "description": "Красивый цветной вывод в терминале, форматирование таблиц, прогресс-бары.",
        "category": "Utilities",
        "docs_url": "https://rich.readthedocs.io"
    },
    {
        "name": "requests",
        "description": "Удобная HTTP-библиотека для работы с REST API и веб-запросами.",
        "category": "Networking",
        "docs_url": "https://requests.readthedocs.io"
    },
    {
        "name": "pydantic",
        "description": "Валидация данных и сериализация моделей на базе аннотаций типов Python.",
        "category": "Core & Types",
        "docs_url": "https://docs.pydantic.dev"
    },
    {
        "name": "aiohttp",
        "description": "Асинхронный HTTP-клиент и веб-сервер для asyncio.",
        "category": "Networking",
        "docs_url": "https://docs.aiohttp.org"
    },
    {
        "name": "scipy",
        "description": "Научные алгоритмы: оптимизация, интегралы, статистика, обработка сигналов.",
        "category": "Data & Math",
        "docs_url": "https://scipy.org"
    },
    {
        "name": "scikit-learn",
        "description": "Классическое машинное обучение: классификация, регрессия, кластеризация и метрики.",
        "category": "Machine Learning",
        "docs_url": "https://scikit-learn.org"
    },
    {
        "name": "seaborn",
        "description": "Статистическая визуализация данных поверх Matplotlib с готовыми палитрами.",
        "category": "Visualization",
        "docs_url": "https://seaborn.pydata.org"
    },
    {
        "name": "networkx",
        "description": "Анализ графов и сетей: кратчайшие пути Дейкстры, центральность, клики.",
        "category": "Algorithms & Graphs",
        "docs_url": "https://networkx.org"
    },
    {
        "name": "beautifulsoup4",
        "description": "Быстрый парсинг HTML/XML документов и извлечение данных из веб-страниц.",
        "category": "Web & Scraping",
        "docs_url": "https://www.crummy.com/software/BeautifulSoup/"
    },
    {
        "name": "httpx",
        "description": "Современный sync/async HTTP-клиент с поддержкой HTTP/2 и строгой типизацией.",
        "category": "Networking",
        "docs_url": "https://www.python-httpx.org"
    },
    {
        "name": "sympy",
        "description": "Символьная математика: производные, интегралы, пределы и решение уравнений.",
        "category": "Data & Math",
        "docs_url": "https://www.sympy.org"
    },
    {
        "name": "loguru",
        "description": "Элегантное и структурированное логирование с цветным выводом без boilerplate.",
        "category": "Utilities",
        "docs_url": "https://loguru.readthedocs.io"
    },
    {
        "name": "psutil",
        "description": "Мониторинг ресурсов системы: загрузка CPU, использование памяти процессами и диск.",
        "category": "System & OS",
        "docs_url": "https://psutil.readthedocs.io"
    },
    {
        "name": "pytest",
        "description": "Промышленный стандарт для написания чистых и масштабируемых тестов.",
        "category": "Testing",
        "docs_url": "https://docs.pytest.org"
    }
]


class PackageActionRequest(BaseModel):
    package: str


@router.get("/list")
async def get_installed():
    """Lists installed packages in sandbox virtual environment."""
    packages = await list_installed_packages()
    return {"packages": packages, "total": len(packages)}


@router.get("/popular")
async def get_popular():
    """Returns curated popular libraries."""
    return {"packages": POPULAR_PACKAGES}


@router.post("/install")
async def run_pip_install(payload: PackageActionRequest):
    """Installs a package via pip in sandbox venv."""
    if not payload.package.strip():
        raise HTTPException(status_code=400, detail="Package name cannot be empty")

    result = await install_package(payload.package)
    return result


@router.post("/uninstall")
async def run_pip_uninstall(payload: PackageActionRequest):
    """Uninstalls a package via pip from sandbox venv."""
    if not payload.package.strip():
        raise HTTPException(status_code=400, detail="Package name cannot be empty")

    result = await uninstall_package(payload.package)
    return result
