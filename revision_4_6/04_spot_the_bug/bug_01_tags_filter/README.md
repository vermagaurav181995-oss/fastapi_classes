# Bug 01: Tag filter ignores the tags

## Symptom
A shop owner says the tag filter "doesn't work": whatever tags they pick, they always get every product back. No error, just the full list.

## Reproduce it
1. Open `/docs` → **GET /filter**. Look closely at how Swagger asks for `tag`. Is it where you'd expect a query parameter?
2. Call `GET /filter?tag=music`. You get all 4 products, but only `headphones` and `guitar` have the `music` tag.
3. Call `GET /filter?tag=music&tag=school`: same full list.

## Expected behavior
`GET /filter?tag=music` → only `headphones` and `guitar`.

## Run it
```bash
cd bug_01_tags_filter/buggy
fastapi dev main.py
```
When you think you've found the bug, compare with `fixed/` (same command, from `bug_01_tags_filter/fixed`) and check `../ANSWERS.md`.
