# Playbook — Hotfix fast lane

Still human-gated; compressed. Open a follow-up ticket for process debt.

## Steps

1. **Problem + blast radius** — who/what broken; severity; rollback if already deployed  
2. **Failing regression test** — add/prove failing test first  
3. **Minimal fix** — smallest change; no refactors  
4. **Review** — correctness + safety  
5. **Deploy + verify** — health + targeted checks  
6. **Follow-up** — ticket for full Analysis/Design/docs debt  

## Read from cache

- Baseline/boundaries if the area is known; otherwise minimal targeted read
- Related risks

## Produce

- Short artifacts (can reuse intake/test/implement/review/deploy/verify templates, marked `hotfix`)
- Follow-up ticket id in retro-style note

## Summary format

```text
Hotfix: <id>
Blast radius: …
Test: <path> (failing then green)
Fix: <PR>
Verify: …
Follow-up: <ticket>
Ask: Approve | Reject
```
