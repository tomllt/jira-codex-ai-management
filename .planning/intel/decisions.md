# Ingested Decisions

- Jira remains the single source of truth for task state and audit history
- Codex only consumes tasks that are explicitly prepared for execution inside the Sprint workflow
- Planning and execution contracts remain structured JSON artifacts
- Brownfield migration keeps `scripts/` as compatibility entry points while introducing `src/jira_codex`
