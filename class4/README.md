# Class 4

## Setup

```bash
cd class4
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

| Example | Command |
|---|---|
| 01 | `cd 01_query_validation && fastapi dev main.py` |
| 02 | `cd 02_path_validation && fastapi dev main.py` |
| 03 | `cd 03_headers_cookies && fastapi dev main.py` |
| 04 | `cd 04_form_and_upload && fastapi dev main.py` |
| 05 | `cd 05_patch_partial_update && fastapi dev main.py` |
| 06 | `cd 06_model_validator_email && fastapi dev main.py` |
| 07 | `cd 07_status_and_list_response && fastapi dev main.py` |
| 08 | `cd 08_custom_exceptions && fastapi dev main.py` |
| 09 | `cd 09_depends_basics && fastapi dev main.py` |
| 10 | `cd 10_class_and_sub_dependencies && fastapi dev main.py` |
| 11 | `cd 11_yield_dependency && fastapi dev main.py` |
| 12 | `cd 12_router_level_dependencies && fastapi dev main.py` |
| 13 | `cd 13_mini_project_bookstore && fastapi dev main.py` |
| Practice | `cd practice && fastapi dev task01_search.py` |

Open http://127.0.0.1:8000/docs

## Tests

```bash
pip install pytest
pytest -v test_all_examples.py
```
