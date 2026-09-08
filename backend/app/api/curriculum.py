from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.grader import evaluate_lesson_submission
from app.data.curriculum import (
    ALL_MODULES,
    get_all_modules_summary,
    get_lesson_by_id,
)

router = APIRouter(prefix="/curriculum", tags=["curriculum"])


class EvaluationRequest(BaseModel):
    code: str
    timeout: Optional[float] = 12.0


@router.get("/modules")
async def list_modules():
    """Returns catalog of all 10 modules with lesson listings and metadata."""
    return {
        "modules": get_all_modules_summary(),
        "total_modules": len(ALL_MODULES)
    }


@router.get("/lessons/{lesson_id}")
async def get_lesson_detail(lesson_id: str):
    """Returns details for a single lesson."""
    lesson = get_lesson_by_id(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail=f"Lesson '{lesson_id}' not found")

    # Hide full solution and raw test code in the initial fetch
    return {
        "id": lesson["id"],
        "module_id": lesson["module_id"],
        "module_title": lesson["module_title"],
        "title": lesson["title"],
        "difficulty": lesson["difficulty"],
        "estimated_minutes": lesson["estimated_minutes"],
        "theory_md": lesson["theory_md"],
        "task_description": lesson["task_description"],
        "starter_code": lesson["starter_code"],
        "total_hints": len(lesson.get("hints", [])),
        "has_solution": bool(lesson.get("solution")),
    }


@router.get("/lessons/{lesson_id}/hints/{level}")
async def get_lesson_hint(lesson_id: str, level: int):
    """
    Returns progressive hint by level:
    Level 1: Conceptual clue
    Level 2: Algorithmic & structural hint
    Level 3: Exact signature / code pattern
    """
    lesson = get_lesson_by_id(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail=f"Lesson '{lesson_id}' not found")

    hints = lesson.get("hints", [])
    matched = next((h for h in hints if h["level"] == level), None)
    if not matched:
        raise HTTPException(
            status_code=404,
            detail=f"Hint level {level} not available for lesson '{lesson_id}'"
        )

    return {
        "lesson_id": lesson_id,
        "level": level,
        "title": matched["title"],
        "content": matched["content"],
        "total_hints": len(hints)
    }


@router.get("/lessons/{lesson_id}/solution")
async def get_lesson_solution(lesson_id: str):
    """Returns verified reference solution and architectural explanation."""
    lesson = get_lesson_by_id(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail=f"Lesson '{lesson_id}' not found")

    if not lesson.get("solution"):
        raise HTTPException(status_code=404, detail="Solution not available for this lesson")

    return {
        "lesson_id": lesson_id,
        "solution": lesson["solution"],
        "title": lesson["title"]
    }


@router.post("/lessons/{lesson_id}/evaluate")
async def evaluate_lesson(lesson_id: str, payload: EvaluationRequest):
    """Evaluates user code against the automated test suite."""
    lesson = get_lesson_by_id(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail=f"Lesson '{lesson_id}' not found")

    test_code = lesson.get("test_suite_code", "")
    if not test_code:
        raise HTTPException(status_code=400, detail="No test suite configured for this lesson")

    results = await evaluate_lesson_submission(
        user_code=payload.code,
        test_suite_code=test_code,
        timeout=payload.timeout or 12.0
    )
    return results
