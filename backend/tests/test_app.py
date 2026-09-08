import os
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Ensure backend root is on sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_curriculum_catalog():
    response = client.get("/api/curriculum/modules")
    assert response.status_code == 200
    data = response.json()
    assert "modules" in data
    assert len(data["modules"]) == 10
    first_mod = data["modules"][0]
    assert first_mod["id"] == "module_1"
    assert len(first_mod["lessons"]) > 0


def test_lesson_detail_and_hints():
    lesson_id = "m1_l1_references_mutability"
    # Detail
    res = client.get(f"/api/curriculum/lessons/{lesson_id}")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == lesson_id
    assert "theory_md" in data
    assert "task_description" in data
    assert data["total_hints"] == 3

    # Progressive Hints: Level 1, 2, 3
    for lvl in (1, 2, 3):
        h_res = client.get(f"/api/curriculum/lessons/{lesson_id}/hints/{lvl}")
        assert h_res.status_code == 200
        h_data = h_res.json()
        assert h_data["level"] == lvl
        assert len(h_data["content"]) > 0

    # Solution
    sol_res = client.get(f"/api/curriculum/lessons/{lesson_id}/solution")
    assert sol_res.status_code == 200
    sol_data = sol_res.json()
    assert "safe_accumulator" in sol_data["solution"]


def test_evaluate_correct_solution():
    lesson_id = "m1_l1_references_mutability"
    # Fetch verified solution
    sol_res = client.get(f"/api/curriculum/lessons/{lesson_id}/solution")
    solution_code = sol_res.json()["solution"]

    # Submit to grader
    eval_res = client.post(
        f"/api/curriculum/lessons/{lesson_id}/evaluate",
        json={"code": solution_code}
    )
    assert eval_res.status_code == 200
    eval_data = eval_res.json()
    assert eval_data["all_passed"] is True
    assert eval_data["total_tests"] == 3
    assert eval_data["passed_tests"] == 3


def test_evaluate_failing_solution():
    lesson_id = "m1_l1_references_mutability"
    broken_code = """
def safe_accumulator(item, bucket=None, copy_mode=False):
    return [999]  # Incorrect output!
"""
    eval_res = client.post(
        f"/api/curriculum/lessons/{lesson_id}/evaluate",
        json={"code": broken_code}
    )
    assert eval_res.status_code == 200
    eval_data = eval_res.json()
    assert eval_data["all_passed"] is False


def test_code_execution():
    code = """
import sys
x = 10 + 25
print(f"Computed sum: {x}")
"""
    res = client.post("/api/execute/code", json={"code": code})
    assert res.status_code == 200
    data = res.json()
    assert data["returncode"] == 0
    assert "Computed sum: 35" in data["stdout"]


def test_file_manager():
    # 1. Get file tree
    tree_res = client.get("/api/files/tree")
    assert tree_res.status_code == 200
    assert "files" in tree_res.json()

    # 2. Create a test file
    create_res = client.post("/api/files/create", json={
        "path": "test_script.py",
        "initial_content": "msg = 'Hello from PyDeep'\nprint(msg)\n"
    })
    assert create_res.status_code == 200

    # 3. Read the test file
    read_res = client.get("/api/files/read?path=test_script.py")
    assert read_res.status_code == 200
    assert "Hello from PyDeep" in read_res.json()["content"]

    # 4. Execute the created file
    exec_res = client.post("/api/execute/file", json={"file_path": "test_script.py"})
    assert exec_res.status_code == 200
    assert "Hello from PyDeep" in exec_res.json()["stdout"]

    # 5. Delete the test file
    del_res = client.delete("/api/files/delete?path=test_script.py")
    assert del_res.status_code == 200


def test_packages_api():
    pop_res = client.get("/api/packages/popular")
    assert pop_res.status_code == 200
    packages = pop_res.json()["packages"]
    assert len(packages) > 0
    names = [p["name"] for p in packages]
    assert "numpy" in names
    assert "matplotlib" in names


def test_spa_index():
    res = client.get("/")
    assert res.status_code == 200
    assert "<!doctype html>" in res.text.lower()


if __name__ == "__main__":
    pytest.main(["-v", __file__])

