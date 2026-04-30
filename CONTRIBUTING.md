# Contributing

Thanks for your interest in contributing to Jira + Codex AI Management.

This repository is currently a private, invite-only prototype workspace. The guidance below is intended to make collaboration smoother for invited contributors today and easier to reuse if the repository becomes public later.

## What Contributions Are Welcome

The following kinds of contributions are welcome:

- Bug fixes
- Documentation improvements
- CI or GitHub template improvements
- Focused code changes
- Well-scoped feature work

## When To Open An Issue First

Please open an issue before starting work if your change touches any of the following:

- Jira governance boundaries
- Codex execution semantics
- Orchestrator architecture
- Large refactors
- New end-to-end workflow behavior

For small documentation updates, isolated bug fixes, or narrow CI/template improvements, opening a PR directly is fine.

## Development Expectations

Keep changes focused.

- Prefer small, reviewable PRs over broad bundles of unrelated work
- Do not mix behavior changes and cosmetic cleanup unless they are tightly coupled
- Preserve the repository's current prototype boundaries unless the change is explicitly intended to revisit them

## Local Verification

Before opening a PR, run the baseline local checks:

```bash
python -m py_compile scripts/*.py
python scripts/orchestrator.py --help
python scripts/orchestrator.py validate ai-plan examples/sample-ai-plan.json
python scripts/orchestrator.py validate execution-result examples/sample-execution-result.json
```

If your change touches Jira integration, Codex execution behavior, task preparation, or writeback logic, include additional validation notes in the PR describing:

- what you tested
- what environment assumptions were required
- what you could not verify locally

## Pull Request Expectations

Use the pull request template and explain:

- what changed
- why it changed
- how you verified it
- what risks or limitations remain

If your change intentionally leaves follow-up work, state that explicitly.

## Repository Hygiene

Do not commit:

- `.env`
- secrets, credentials, or tokens
- private Jira payloads copied from local systems
- local-only absolute paths unless they are already part of a documented example
- generated caches or machine-specific artifacts

## Need Help?

If you are not sure whether a change fits the repository boundary, open an issue first and describe the proposed direction before implementing it.
