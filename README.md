# Agentic Build System

A portable, **tech-stack-agnostic** kit for human-in-the-loop agentic delivery.

Agents produce small stage artifacts. Humans approve each stage before the next. Failures are fixed in the current stage (fix-forward). Default order: **contracts → TDD tests → implement → UI polish**.

## What you get

| Path | Role |
|------|------|
| [`WORKFLOW.md`](./WORKFLOW.md) | Locked SDLC stages + principles |
| [`USAGE.md`](./USAGE.md) | Apply to greenfield or brownfield projects |
| [`INSTALL.md`](./INSTALL.md) | Install this kit into another git repo |
| [`feature-types.md`](./feature-types.md) | Which stages are required / optional |
| [`templates/`](./templates/) | Stage artifact templates (diagram slots + approval) |
| [`playbooks/`](./playbooks/) | Agent playbooks per stage |
| [`context/`](./context/) | SQLite schema + Python CLI (stdlib only) |
| [`adr/`](./adr/) | ADR template + index |
| [`diagrams/`](./diagrams/) | As-is / to-be Mermaid examples + naming |

## Greenfield vs brownfield

| Mode | First steps |
|------|-------------|
| **Greenfield** | Intake → Analysis → Requirements → Design… Skip stage **0b** (architecture baseline). |
| **Brownfield** | Intake → **0b Architecture baseline** (as-is UML + ADR harvest) → then normal stages. Preserve confirmed ADRs unless a human approves an amendment. |

## Quick start

1. Install the kit into your repo ([`INSTALL.md`](./INSTALL.md) — recommended: GitHub template or sparse copy).
2. Init the context DB:

   ```bash
   python3 context/abs_context.py init --db .abs/context.db
   ```

3. Pick feature type from [`feature-types.md`](./feature-types.md); open a feature branch.
4. For each required stage: follow `playbooks/<stage>.md`, fill `templates/<stage>.md`, get human **Approve** / **Approve with notes** / **Reject**.
5. Upsert decisions, diagrams, and artifacts into the context DB; print a load pack before the next agent turn:

   ```bash
   python3 context/abs_context.py load-pack --db .abs/context.db --feature <id>
   ```

## Locked defaults

- Human gate every stage; never batch-approve remaining stages
- Threat review when auth / data / network / PII change; else a short “no new trust boundary” note
- SQLite context cache; agents read cache before crawling the repo
- UML current vs proposed with a short delta caption
- Refactors incomplete until touched docs/diagrams are updated

## Requirements

- Git
- Python 3.9+ (context CLI uses stdlib `sqlite3` only — no pip install)
- Mermaid-capable Markdown viewer (optional; diagrams stay as fenced code)

## Source / publish

- Target GitHub: `https://github.com/ThiwankaS/build_system_kit.git` (SSH: `git@github.com:ThiwankaS/build_system_kit.git`)
- **Publish pending** SCM connect — until then use this tree from Project Context

## Non-goals

- Not a CI product, IDE plugin, or language-specific scaffold
- Does not assume React, Java, or any particular framework
