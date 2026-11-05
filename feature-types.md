# Feature types — required vs optional stages

Legend: **R** = required · **O** = optional / skip if N/A · **F** = fast-lane substitute · **—** = skip

| Stage | feature | fix | chore | docs | hotfix |
|-------|---------|-----|-------|------|--------|
| 0 Intake | R | R | R (short) | R (short) | F (problem + blast radius) |
| 0b Architecture baseline | R* | R* | R* | R* | R* if touching unknown area |
| 1 Analysis | R | R (narrow) | O | O | — (folded into intake) |
| 2 Requirements & AC | R | R | O | O (what docs change) | O |
| 3 Design | R | R (minimal) | O | — | — |
| 4 Threat & privacy | R† | R† | O† | — | R† |
| 5 UI/UX | O‡ | O‡ | — | — | — |
| 6 Test design (TDD) | R | R | O | — | F (failing regression) |
| 7 Implementation | R | R | R | R (doc edits) | F (minimal fix) |
| 8 Review | R | R | R | R | F |
| 9 Refactor | O | O | O | — | — |
| 10 QA | R | R | O | O | O (smoke) |
| 11 Docs & runbooks | R | O | O | R | O (follow-up OK) |
| 12 Release prep | R | O | O | — | F (minimal checklist) |
| 13 Deploy | R | O | — | — | F |
| 14 Post-deploy verify | R | O | — | — | F |
| 15 Retro & memory | R | O | O | O | R (capture debt) |

\* **0b** required on **first use** of an existing repo (or when a large unknown area is first touched). Skip only for true greenfield.  
† Full threat review when auth / data stores / network-trust / PII change; otherwise short **“no new trust boundary”** note (counts as completing the stage).  
‡ Skip UI/UX for non-UI changes; keep API contract notes if UX is affected indirectly. UI **polish** follows tests per locked order.

## Notes

- **chore / docs:** may skip UI/UX, deploy, and post-deploy. Still human-gated for stages that run.
- **hotfix:** use [`playbooks/hotfix.md`](./playbooks/hotfix.md); open a follow-up ticket for skipped process debt.
- **feature:** default full path; contracts → TDD → implement → UI polish.
- Always record skips in the feature’s Intake or Design artifact (“skipped stage N because …”).
