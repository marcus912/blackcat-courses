# Week 03 — Python first-class functions

- **Date:** 2026-05-23 (Sat)
- **Stage:** Python language deep-dive
- **Focus (重點看):** 《Python 一級函式修煉手冊》 — adapted from Luciano Ramalho, *Fluent Python*

## Source courses

- [x] Fluent Python ch. 7–9 (first-class functions, type hints, decorators & closures)
- [x] See condensed reference: [`python-first-class-functions.md`](./python-first-class-functions.md)

## Homework (動手)

What was built:

> **黑貓算命** — a tiny deterministic fortune-teller web app (Flask) that puts five
> first-class-function syntaxes to work: iterable unpacking, dictionary unpacking,
> callables (`__call__`), `*args/**kwargs`, and a registration decorator. Enter a
> name + birthday and the black cat returns your 生肖, 幸運數字, 幸運色 and 今日宜.
> Readings are seeded by name+birthday (no RNG) so the page is reproducible and the
> 19-test pytest suite is stable.

How to run:

```bash
cd homework/fortune-web
uv sync                            # self-contained uv project (own pyproject.toml + uv.lock)
uv run flask --app app run         # http://127.0.0.1:5000
uv run pytest                      # 19 tests
```

## Demo

![demo](./demo/demo.gif)

## Takeaways

1. A **registration decorator** (`@fortune`) lets readings register themselves at
   import time — the app never maintains a hand-written list, and adding a reading
   is one decorated function.
2. An object with `__call__` is the clean way to get a *callable that keeps state* —
   `FortuneTeller` remembers its consultation history between calls.
3. `{**a, **b}` merge + `f(**profile)` dispatch make defaults-plus-overrides and
   keyword spreading trivial; `*args/**kwargs` in a wrapper passes any signature through.

## Open questions

- When does a stateful `__call__` object beat a closure, and vice versa?
- Worth adding `functools.singledispatch` to vary a reading by input type?
