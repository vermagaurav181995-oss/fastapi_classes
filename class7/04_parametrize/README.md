# 04: Parametrize

## What it shows
`@pytest.mark.parametrize` runs one test function once per input:
- `test_invalid_book_returns_422` × 6: empty title, 201-char title, price 0, price −5, missing price, missing title
- `test_valid_ids_return_the_right_book` × 3: several argument names at once (`("book_id", "expected_title")`)
- `test_bad_ids` × 4: `0`, `-1`, `999`, `"abc"`
- `pytest.param(..., id="price-zero")` gives each case a readable name in the output

## Setup
No `.env` needed.

## Run
```bash
cd 04_parametrize
pytest -v
```

## Expected output
```
test_validation.py::test_invalid_book_returns_422[empty-title] PASSED
test_validation.py::test_invalid_book_returns_422[title-201-chars] PASSED
test_validation.py::test_invalid_book_returns_422[price-zero] PASSED
...
========================= 14 passed =========================
```
