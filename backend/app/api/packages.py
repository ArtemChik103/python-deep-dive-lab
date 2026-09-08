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
