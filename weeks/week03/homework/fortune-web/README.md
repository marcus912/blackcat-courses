# 黑貓算命 · Fortune-Teller (week03 homework)

A tiny **算命** web app that exercises five first-class-function syntaxes from
this week's notes ([`python-first-class-functions.md`](../../python-first-class-functions.md)).
Enter a name + birthday → the black cat returns your 生肖, 幸運數字, 幸運色, and
今日宜. Every reading is **deterministic** (seeded by name+birthday, no RNG), so
the page is reproducible and the tests are stable.

## The 5 required syntaxes → where they live

| # | Syntax | File | What to look at |
|---|--------|------|-----------------|
| 1 | **iterable unpacking** | `fortune/profile.py` | `year, month, day = ...` and `surname, *given = name` |
| 2 | **dictionary unpacking** | `fortune/profile.py`, `fortune/teller.py` | `{**DEFAULTS, **overrides}` merge; `reading(**profile)` at the call site |
| 3 | **callable** | `fortune/teller.py` | `FortuneTeller.__call__` (stateful, keeps a history) + a `callable()` guard |
| 4 | **`*args` / `**kwargs`** | `fortune/decorators.py`, `fortune/readings.py` | wrapper `def wrapper(*args, **kwargs)`; readings take `**profile` |
| 5 | **decorators** | `fortune/decorators.py` | `@fortune(label)` registration decorator + `@log_call` with `functools.wraps` |

## Layout

```
fortune-web/
├── app.py              Flask routes (thin — validate + render only)
├── fortune/
│   ├── decorators.py   @fortune registry + @log_call
│   ├── profile.py      build_profile() — unpacking + validation
│   ├── readings.py     生肖 / 幸運數字 / 幸運色 / 今日宜 (each @fortune-registered)
│   └── teller.py       FortuneTeller — the stateful callable
├── templates/index.html
├── static/style.css
└── tests/test_fortune.py
```

## Run

Self-contained [uv](https://docs.astral.sh/uv/) project (its own `pyproject.toml`
+ `uv.lock`; does **not** inherit from the repo-root uv project).

```bash
cd weeks/week03/homework/fortune-web
uv sync                                # create .venv from the lockfile
uv run flask --app app run             # http://127.0.0.1:5000
```

## Test

```bash
uv run pytest                          # 19 tests
```

## How it works

1. Importing `fortune` runs the `@fortune(...)` decorators in `readings.py` —
   decorators fire at **import time**, registering each reading into a list.
2. A `FortuneTeller` instance reads that registry. Calling it (`teller(profile)`)
   loops the readings, spreading the profile dict into each via `**profile`, and
   appends the result to its history.
3. `app.py` builds the profile from the form (merging defaults via dict
   unpacking), calls the teller, and renders the labelled results.
