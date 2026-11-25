# 01: pytest Basics

## What it shows
- pytest finds files named `test_*.py` and runs every function named `test_*`.
- `assert` checks a condition; pytest shows the actual and expected values when it fails.
- The **Arrange → Act → Assert** structure.
- `@pytest.mark.skip` and reading a failure report (`test_fail_on_purpose.py`).

## Setup
No `.env` needed.

## Run
```bash
cd 01_pytest_basics
pytest -v
pytest -v -k negative        # only tests whose name contains "negative"
```

## Expected output
```
test_fail_on_purpose.py::test_add_is_wrong_on_purpose SKIPPED (Remove this line to see ...)
test_math.py::test_add_two_positive_numbers PASSED
test_math.py::test_add_negative_numbers PASSED
========================= 2 passed, 1 skipped =========================
```
Now delete the `@pytest.mark.skip(...)` line in `test_fail_on_purpose.py` and run `pytest -v` again:
```
FAILED test_fail_on_purpose.py::test_add_is_wrong_on_purpose - assert 5 == 6
E       assert 5 == 6
E        +  where 5 = add(2, 3)
```
pytest shows the failing line, the actual value (`5`, from `add(2, 3)`) and the expected value (`6`).
