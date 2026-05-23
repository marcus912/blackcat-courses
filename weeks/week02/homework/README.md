# Week 02 homework

Two parts.

## (a) Linked-List mini game — _Cache Crash_

A web reaction game built on **LRU Cache (LeetCode 146)** — the cache slots ARE the playfield.

- **Activity diagram** — `a-linked-list-game/activity-diagram.mmd`
- **Class diagram** — `a-linked-list-game/class-diagram.mmd`
- **Working code** — pure HTML/CSS/vanilla JS modules, no build step (`lru.js`, `game.js`, `index.html`, `style.css`)

Folder: [`a-linked-list-game/`](./a-linked-list-game/) — see its README for rules, run instructions, and the LeetCode 146 mapping.

## (b) Sequence diagram from pygame source

Given a pygame collision-simulation script (`b-sequence-diagram/source.py`), produce a sequence diagram describing one frame of the main loop.

Folder: [`b-sequence-diagram/`](./b-sequence-diagram/)

Files:

- `source.py` — the original script being analyzed
- `sequence.mmd` — Mermaid sequence diagram (canonical, renders on GitHub)
- `sequence.puml` — PlantUML version for the classic UML look (printable)
- `README.md` — explanation of how the diagram maps to the code

## Tooling decision

| Format | Why |
|---|---|
| **Mermaid (canonical)** | Renders inline on GitHub portfolio; plain-text diff-friendly |
| **PlantUML (parallel)** | Closer to the classic StarUML aesthetic when the instructor wants the "traditional" UML look |
| StarUML `.mdj` | Skipped — binary, doesn't diff, doesn't render in GitHub |
