# Playbook — 0b Architecture baseline

## Read from cache

- Existing `architecture_baseline`, `decisions`, `boundaries` (may be empty)
- `repo_index` if present

## Produce

- As-is component + sequence diagrams
- ADR harvest table → `upsert-decision` (prefer `inferred` until confirmed)
- Boundaries text → `upsert-boundary`
- `templates/00b-architecture-baseline.md`
- On approve: `upsert-baseline`

## Rules

- Do not “improve” architecture in this stage
- Treat inferred ADRs as constraints until human confirms or rejects

## Stop for human

Summary: module map caption, decision counts (confirmed/inferred), top risks, ask to confirm baseline.
