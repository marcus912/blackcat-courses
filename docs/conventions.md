# Conventions

## Folder names

- Weeks are `weekNN` (zero-padded, `week01` … `week26`). Topic lives inside the README, not the folder name, so the curriculum can change without renames.

## Per-week structure

```
weeks/weekNN/
├── README.md     ← topic, date, source courses, what I learned, link to demo
├── notes.md      ← main-course notes (14:00–16:00)
├── homework/     ← 動手 deliverable (17:30–18:00). Self-contained — bring your own deps.
└── demo/         ← screenshots, demo.gif, asciinema cast
```

`homework/` is self-contained: it owns its own `package.json`, `requirements.txt`, `Dockerfile`, etc. No shared root manifest — weeks use different stacks.

## Week README template

Use `shared/templates/week-README.md`. Required fields:

- `# Week NN — <topic>`
- **Date** (Saturday in `YYYY-MM-DD`)
- **Topic / focus**
- **Source courses** (links / titles of reference videos watched)
- **Homework** (what was built, how to run)
- **Demo** (link to `demo/demo.gif` or screenshot)
- **Takeaways** (3 bullets — what would I tell someone in one minute?)

## Demo

- Prefer `demo.gif` < 5 MB or a screenshot for inline preview.
- Long videos (`.mp4`/`.mov`) are gitignored — host on YouTube/Loom and link in the README.
- For CLI work: `asciinema` cast committed as `demo.cast`.

## Commit messages

Follow `<type>: <description>` (feat / fix / docs / chore). Prefix weekly work with the week number:

```
feat(week03): k8s minikube deploy of week02 image
docs(week01): add takeaways and demo gif
```
