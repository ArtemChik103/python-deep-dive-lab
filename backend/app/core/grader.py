import json
import re
from typing import Any, Dict, List, Optional

from app.core.runner import run_code_or_file

GRADER_DELIMITER_START = "---PYDEEP_GRADER_JSON_START---"
GRADER_DELIMITER_END = "---PYDEEP_GRADER_JSON_END---"

HARNESS_TEMPLATE = '''
import sys
import json
import time
import traceback

__PYDEEP_TEST_RESULTS__ = []

def pydeep_test(name: str, expected: any = None):
    """Decorator to mark and execute a grader test case."""
    def decorator(fn):
        start = time.perf_counter()
        res = {
            "name": name,
            "passed": False,
            "expected": repr(expected) if expected is not None else None,
            "actual": None,
            "error": None,
            "duration_ms": 0
        }
        try:
            actual = fn()
            res["actual"] = repr(actual) if actual is not None else None
            if expected is not None:
                if actual == expected:
                    res["passed"] = True
                else:
                    res["passed"] = False
                    res["error"] = f"Assertion failed: expected {expected!r}, but received {actual!r}"
            else:
                res["passed"] = True
        except AssertionError as ae:
            res["error"] = str(ae) or "Assertion failed"
            res["passed"] = False
        except Exception as e:
            res["error"] = f"{type(e).__name__}: {str(e)}"
            res["passed"] = False
        
        res["duration_ms"] = round((time.perf_counter() - start) * 1000, 2)
        __PYDEEP_TEST_RESULTS__.append(res)
        return fn
    return decorator

# ==== USER CODE BEGIN ====
__USER_CODE_PLACEHOLDER__
# ==== USER CODE END ====

# ==== TEST SUITE BEGIN ====
__TEST_SUITE_PLACEHOLDER__
# ==== TEST SUITE END ====

# Output results
print("\\n" + "__START_TAG_PLACEHOLDER__")
print(json.dumps(__PYDEEP_TEST_RESULTS__))
print("__END_TAG_PLACEHOLDER__")
'''


async def evaluate_lesson_submission(
    user_code: str,
    test_suite_code: str,
    timeout: float = 12.0
) -> Dict[str, Any]:
    """
    Combines user code with test harness and runs in the sandbox environment.
    Parses and returns structured test case results.
    """
    full_code = (
        HARNESS_TEMPLATE
        .replace("__USER_CODE_PLACEHOLDER__", user_code)
        .replace("__TEST_SUITE_PLACEHOLDER__", test_suite_code)
        .replace("__START_TAG_PLACEHOLDER__", GRADER_DELIMITER_START)
        .replace("__END_TAG_PLACEHOLDER__", GRADER_DELIMITER_END)
    )

    exec_result = await run_code_or_file(code=full_code, timeout=timeout)
    stdout = exec_result.get("stdout", "")
    stderr = exec_result.get("stderr", "")

    # Parse grader JSON
    test_cases: List[Dict[str, Any]] = []
    clean_stdout = stdout
    
    if GRADER_DELIMITER_START in stdout and GRADER_DELIMITER_END in stdout:
        try:
            parts = stdout.split(GRADER_DELIMITER_START)
            clean_stdout = parts[0].rstrip()
            json_part = parts[1].split(GRADER_DELIMITER_END)[0].strip()
            test_cases = json.loads(json_part)
        except Exception as e:
            stderr += f"\nFailed to parse test results: {str(e)}"

    total_tests = len(test_cases)
    passed_tests = sum(1 for tc in test_cases if tc.get("passed", False))
    all_passed = (total_tests > 0) and (passed_tests == total_tests)

    # If syntax error or unhandled exception happened before tests ran
    if total_tests == 0 and (exec_result.get("returncode", 0) != 0 or stderr):
        all_passed = False

    return {
        "all_passed": all_passed,
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "test_cases": test_cases,
        "stdout": clean_stdout,
        "stderr": stderr,
        "execution_time_ms": exec_result.get("execution_time_ms", 0),
        "timed_out": exec_result.get("timed_out", False)
    }
