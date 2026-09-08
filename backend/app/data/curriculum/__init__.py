from typing import Any, Dict, List, Optional

from app.data.curriculum.module0_absolute_basics import MODULE_0
from app.data.curriculum.module1_basics import MODULE_1
from app.data.curriculum.module2_collections import MODULE_2
from app.data.curriculum.module3_oop_internals import MODULE_3
from app.data.curriculum.module4_iterators_generators import MODULE_4
from app.data.curriculum.module5_decorators_context import MODULE_5
from app.data.curriculum.module6_asyncio import MODULE_6
from app.data.curriculum.module7_metaprogramming import MODULE_7
from app.data.curriculum.module8_cpython_bytecode import MODULE_8
from app.data.curriculum.module9_typing_protocols import MODULE_9
from app.data.curriculum.module10_production import MODULE_10

ALL_MODULES: List[Dict[str, Any]] = [
    MODULE_0,
    MODULE_1,
    MODULE_2,
    MODULE_3,
    MODULE_4,
    MODULE_5,
    MODULE_6,
    MODULE_7,
    MODULE_8,
    MODULE_9,
    MODULE_10
]


def get_all_modules_summary() -> List[Dict[str, Any]]:
    """Returns modules with brief lesson summaries (excluding test code and full solutions)."""
    summaries = []
    for mod in ALL_MODULES:
        lessons_summary = []
        for lsn in mod["lessons"]:
            lessons_summary.append({
                "id": lsn["id"],
                "module_id": mod["id"],
                "title": lsn["title"],
                "difficulty": lsn["difficulty"],
                "estimated_minutes": lsn["estimated_minutes"],
                "hints_count": len(lsn.get("hints", [])),
                "has_solution": bool(lsn.get("solution")),
            })
        summaries.append({
            "id": mod["id"],
            "title": mod["title"],
            "description": mod["description"],
            "order": mod["order"],
            "total_lessons": len(lessons_summary),
            "lessons": lessons_summary
        })
    return summaries


def get_lesson_by_id(lesson_id: str) -> Optional[Dict[str, Any]]:
    """Finds a specific lesson by its id."""
    for mod in ALL_MODULES:
        for lsn in mod["lessons"]:
            if lsn["id"] == lesson_id:
                # Return deep copy or dictionary with lesson info
                return {
                    **lsn,
                    "module_id": mod["id"],
                    "module_title": mod["title"]
                }
    return None
