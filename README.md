# blackcat-courses

Personal learning record for a 26-week course (2026-05-09 → 2026-10-31, every Saturday).

This repo documents weekly notes, homework, and demos. The W26 capstone integrates accumulated work into a single deployable product.

## Layout

| Path | Purpose |
|---|---|
| `weeks/weekNN/` | Per-week notes, homework, and demo (one folder per week, week01–week26) |
| `capstone/` | Final integrated project (filled in toward W26) |
| `docs/roadmap.md` | 26-week status table |
| `docs/conventions.md` | README template, demo conventions |
| `shared/scripts/new-week.sh` | Scaffolds a new week from the template |
| `shared/templates/` | Templates for week README and notes |
| `blog/posts/` | Tech blog drafts (W26 deliverable) |

## Schedule

- Start: 2026-05-09 (Sat)
- End: 2026-10-31 (Sat)
- Cadence: 4 hours every Saturday
- Reference: see [`CourceSchedule.pdf`](./CourceSchedule.pdf) (curriculum is subject to change — folder names use `weekNN` only)

## Workflow

1. Sunday before class: run `./shared/scripts/new-week.sh NN` to scaffold the week.
2. During class (14:00–16:00): take notes in `weeks/weekNN/notes.md`.
3. After class (17:30–18:00): write homework code in `weeks/weekNN/homework/`.
4. End of week: drop screenshots / gif into `weeks/weekNN/demo/` and update `weeks/weekNN/README.md`.
