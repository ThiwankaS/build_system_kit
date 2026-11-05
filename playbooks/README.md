# Agent playbooks

One playbook per stage. Agents: read cache first, produce the template artifact, then a ≤½ page human summary.

| Playbook | Stage |
|----------|-------|
| [`00-intake.md`](./00-intake.md) | 0 |
| [`00b-architecture-baseline.md`](./00b-architecture-baseline.md) | 0b |
| [`01-analysis.md`](./01-analysis.md) | 1 |
| [`02-requirements.md`](./02-requirements.md) | 2 |
| [`03-design.md`](./03-design.md) | 3 |
| [`04-threat-privacy.md`](./04-threat-privacy.md) | 4 |
| [`05-ui-ux.md`](./05-ui-ux.md) | 5 |
| [`06-test-design.md`](./06-test-design.md) | 6 |
| [`07-implementation.md`](./07-implementation.md) | 7 |
| [`08-review.md`](./08-review.md) | 8 |
| [`09-refactor.md`](./09-refactor.md) | 9 |
| [`10-qa.md`](./10-qa.md) | 10 |
| [`11-docs-runbooks.md`](./11-docs-runbooks.md) | 11 |
| [`12-release-prep.md`](./12-release-prep.md) | 12 |
| [`13-deploy.md`](./13-deploy.md) | 13 |
| [`14-post-deploy-verify.md`](./14-post-deploy-verify.md) | 14 |
| [`15-retro.md`](./15-retro.md) | 15 |
| [`hotfix.md`](./hotfix.md) | Hotfix fast lane |

## Summary format (every stage)

```text
Stage: <n> <name>
Feature: <id> (<branch>)
Artifact: <path>
Ask: Approve | Approve with notes | Reject
Highlights:
- …
Risks / asks:
- …
```
