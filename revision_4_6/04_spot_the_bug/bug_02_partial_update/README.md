# Bug 02: Updating the price deletes the name

## Symptom
Changing only the price of an item also wipes out its other fields.

## Reproduce it
1. `GET /items/1` → `{"name": "Pen", "price": 1.5, "in_stock": true}`
2. `PATCH /items/1` with body `{"price": 2.0}`
3. The response is `{"name": null, "price": 2.0, "in_stock": null}`. The name and stock status are gone.

## Expected behavior
`PATCH /items/1` `{"price": 2.0}` → name `Pen` and `in_stock: true` are kept.

## Run it
```bash
cd bug_02_partial_update/buggy
fastapi dev main.py
```
When you think you've found the bug, compare with `fixed/` (same command, from `bug_02_partial_update/fixed`) and check `../ANSWERS.md`.
