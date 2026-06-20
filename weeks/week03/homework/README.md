# Week 03 homework

## What

**黑貓算命 (Fortune-Teller)** — a tiny Flask web app that practises five
first-class-function syntaxes from this week's notes: iterable unpacking,
dictionary unpacking, callables (`__call__`), `*args/**kwargs`, and decorators.
Enter name + birthday → get 生肖 / 幸運數字 / 幸運色 / 今日宜 (deterministic, no RNG).

Folder: [`fortune-web/`](./fortune-web/) — see its README for the syntax→code map.

## Run

```bash
cd fortune-web
uv sync                            # self-contained uv project (own pyproject.toml + uv.lock)
uv run flask --app app run         # http://127.0.0.1:5000
uv run pytest                      # 19 tests
```

## Files

- `fortune-web/fortune/decorators.py` — `@fortune` registration decorator + `@log_call` (`functools.wraps`, `*args/**kwargs`)
- `fortune-web/fortune/profile.py` — `build_profile()`: iterable + dictionary unpacking, input validation
- `fortune-web/fortune/readings.py` — the four readings, each `@fortune`-registered
- `fortune-web/fortune/teller.py` — `FortuneTeller`, a stateful `__call__` object
- `fortune-web/app.py` — Flask routes (thin: validate + render)
- `fortune-web/tests/test_fortune.py` — pytest suite
