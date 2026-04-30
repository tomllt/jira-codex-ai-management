# Security Policy

## Reporting A Vulnerability

Please do **not** report security issues in public GitHub issues.

Use this repository's private GitHub vulnerability reporting flow instead. Submit the report through the repository's Security tab so the maintainer can triage it without exposing sensitive details publicly.

## What To Report Privately

Report privately if the issue involves any of the following:

- Jira credentials, tokens, or authentication handling
- `.env` contents or secrets exposure
- local absolute workdir paths that reveal sensitive repository layout
- copied task or requirement data from private local Jira instances
- real `codex exec` traces or outputs that expose sensitive local repository context
- unsafe command execution or privilege boundary problems

## What Not To Post Publicly

Do not post the following in public issues or PRs:

- passwords, API tokens, or cookies
- private Jira issue content
- internal repository paths from private machines
- execution transcripts that expose sensitive data

If you are unsure whether something is sensitive, treat it as sensitive and use the private reporting path.

## Response Expectations

This repository does not provide a formal SLA, but reported vulnerabilities will be reviewed on a best-effort basis.

When possible, reports should include:

- a short summary
- impact
- reproduction steps
- any mitigation ideas

## Out Of Scope For Formal Guarantees

This repository is a prototype and does not claim enterprise-grade operational guarantees, dedicated on-call coverage, or audited production security controls.
