# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Personal learning portfolio for a 26-week Saturday course (2026-05-09 → 2026-10-31). It is **not** a single application — it is a folder of 26 independent weekly deliverables plus a final capstone. Each `weeks/weekNN/homework/` is self-contained and brings its own stack (its own `package.json`, `requirements.txt`, `Dockerfile`, etc.). There is no root manifest, no monorepo tooling, no shared lockfile.

The curriculum is still changing — folder names use `weekNN` only, and topics live inside each week's `README.md`. Treat the topic in `docs/roadmap.md` as a placeholder until the week is actually done.

## Common commands

Scaffold a new week (idempotent — only creates files that don't exist):

```bash
./shared/scripts/new-week.sh <1-26> "<topic>"
# Example: ./shared/scripts/new-week.sh 3 "Kubernetes intro"
```

The script computes the Saturday date from `week1 = 2026-05-09 + (N-1)*7 days` (uses Python — BSD/GNU `date` flag differences). It renders three templates with `{{NN}}`, `{{topic}}`, `{{YYYY-MM-DD}}` substitutions:

- `shared/templates/week-README.md` → `weeks/weekNN/README.md`
- `shared/templates/week-notes.md` → `weeks/weekNN/notes.md`
- `shared/templates/homework-README.md` → `weeks/weekNN/homework/README.md`

There is no top-level build/test/lint command. Run a week's homework by `cd weeks/weekNN/homework/<part>` and following its local README.

## Structure that matters

- `weeks/weekNN/` — one per week, all 26 already scaffolded. Layout per week:
  - `README.md` — topic, date, source courses, homework summary, demo link, takeaways
  - `notes.md` — main-course notes (14:00–16:00 class block)
  - `homework/` — the deliverable; may contain multiple sub-projects (e.g. `a-…/`, `b-…/` like week02)
  - `demo/` — `demo.gif` / screenshots / `demo.cast`. Large videos (`.mp4`/`.mov`) are gitignored — host externally and link.
- `docs/roadmap.md` — 26-row status table, single source of truth for what's done. Update the row when a week starts/finishes.
- `docs/conventions.md` — required README fields, demo conventions, commit prefix rule.
- `capstone/` — empty until W26; integrates accumulated work into one deployable.
- `blog/posts/` — tech blog drafts (W26 deliverable).

## Conventions to follow

- **Commit prefix:** prefix weekly work with the week number, e.g. `feat(week03): …`, `docs(week01): …`. Types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `perf`, `ci`.
- **Diagrams:** Mermaid is the canonical format (renders inline on GitHub). PlantUML is used in parallel only for the classic UML look (see week02).
- **Demos:** prefer `demo.gif` < 5 MB or a screenshot. `.mp4`/`.mov`/`.zip`/`.tar.gz` are gitignored; do not commit them.
- **No cross-week dependencies:** never edit one week's `homework/` from another week's context. If week N builds on week N-1, copy what's needed in.
