# WORKFLOW — Agentic Build System SDLC

Tech-stack agnostic. Self-contained for offline use. Source of locked defaults: Project `docs/sdlc-workflow.md`.

---

## Principles

1. **Human gate** — each stage ends with a small artifact; stop until approved.
2. **Fix-forward** — failed review stays in that stage; do not skip ahead.
3. **TDD** — failing tests / executable specs approved before production code.
4. **One feature, one branch** — meaningful names; no direct trunk commits.
5. **Context cache** — SQLite facts before full-repo/chat re-reads.
6. **Stack-agnostic** — artifacts and checks, not frameworks.
7. **Diagrams first** — UML (Mermaid/PlantUML) over long prose.
8. **Current vs proposed** — as-is + to-be + short delta before approve.
9. **Brownfield-safe** — preserve ADRs unless human approves change.
10. **Document as you refactor** — touched area leaves better docs, not only cleaner code.

---

## Diagrams (UML-first)

| Need | Preferred diagram |
|------|-------------------|
| Who interacts with what | Use case |
| Runtime flow / requests | Sequence |
| Structure / modules | Component or package |
| Domain objects | Class |
| States / lifecycle | State machine |
| Deploy topology | Deployment |
| Data shape | ER / class |
| User journeys | Activity / flow |

**Current vs proposed:** Analysis, Design, and structure-changing refactors produce:

1. **As-is**  
2. **To-be**  
3. **Delta caption** (3–7 bullets: changes, stays, risks)

---

## Brownfield

### Architecture discovery (stage 0b)

On first engagement (or large unknown area):

1. Map modules, entrypoints, stores, deps → as-is diagrams  
2. Extract ADRs → context `decisions` (`confirmed` / `inferred` / `superseded`)  
3. Human approves architecture baseline  
4. Until approved, treat inferred decisions as **constraints**, not improvement ideas  

### Preserve-by-default

- New work fits confirmed ADRs  
- Changing a confirmed decision needs ADR amendment + human approve  
- Cross-boundary “cleanup” blocked until to-be + ADR update approved  

Agents **must** load baseline + decisions + boundaries before Design or Implementation on existing code.

---

## Stages

| # | Stage | Exit artifact |
|---|--------|---------------|
| 0 | Intake & problem framing | Problem brief + success metrics |
| 0b | Architecture baseline *(existing repos)* | As-is UML + decision list |
| 1 | Analysis | Notes + as-is diagrams + resolved questions |
| 2 | Requirements & AC | Testable user stories / AC |
| 3 | Design | As-is + to-be UML, delta, contracts, ADR updates |
| 4 | Threat & privacy | Threat notes + mitigations (or “no new trust boundary”) |
| 5 | UI/UX *(when UI)* | Flows / wireframes + a11y checklist |
| 6 | Test design (TDD) | Test plan + failing tests/specs |
| 7 | Implementation | Diff on feature branch |
| 8 | Review | Review notes + addressed comments |
| 9 | Refactor | Diff; tests green; docs/diagrams for touch set |
| 10 | QA | QA report + bugs empty or fixed |
| 11 | Docs & runbooks | Changelog + ops notes + arch docs |
| 12 | Release prep | Release checklist signed off |
| 13 | Deploy | Deploy record + health checks |
| 14 | Post-deploy verify | Verification log |
| 15 | Retro & memory update | Retro + context DB / ADR updates |

Stages 4–5 may parallel late design when scope is clear. Skip UI only for non-UI changes. Skip 0b only for true greenfield.

**Locked order:** contracts (Design) → TDD tests → implement → UI polish.

**Threat:** required when auth, data stores, network/trust boundaries, or PII change; else short “no new trust boundary” note.

**Optional by type:** see [`feature-types.md`](./feature-types.md).

---

## Human approval protocol

1. Agent: ≤½ page summary + artifact link  
2. Human: **Approve** / **Approve with notes** / **Reject (fix in this stage)**  
3. Reject → stay on stage  
4. Approve → advance; write outcome to context DB  

Never batch-approve remaining stages.

---

## Git conventions

- Trunk: `main` (or `trunk`) — protected  
- Branches: `feature/…`, `fix/…`, `chore/…`, `docs/…`, `hotfix/…`  
- One primary outcome per branch; PR + CI green + human review before merge  

---

## Context cache (SQLite)

Tables: `projects`, `features`, `decisions`, `architecture_baseline`, `boundaries`, `requirements`, `artifacts`, `diagrams`, `test_map`, `risks`, `repo_index`, `doc_debt`, `run_log`.

**Read order:** baseline → decisions/boundaries → feature → AC/test_map → diagrams → artifacts → targeted code via `repo_index`.

CLI: [`context/abs_context.py`](./context/abs_context.py).

---

## Refactor documentation bar

Incomplete until: diagrams updated or confirmed; module overview if structure moved; public contracts refreshed; ADRs amended if needed; `doc_debt` cleared or deferred by human.

---

## Definition of Done (default)

- [ ] All AC have passing automated tests  
- [ ] Human approved every required stage  
- [ ] Required UML pairs approved and stored  
- [ ] No unapproved ADR/boundary drift  
- [ ] Review comments resolved or deferred  
- [ ] Docs/changelog updated if user/ops-facing; refactor docs bar if refactor ran  
- [ ] CI green on feature branch  
- [ ] Deployed or merge-ready with rollback noted  
- [ ] Post-deploy verify passed (or N/A)  
- [ ] Context DB updated; branch cleaned per policy  

---

## Hotfix fast lane

1. Problem + blast radius  
2. Failing regression test  
3. Minimal fix  
4. Review  
5. Deploy + verify  
6. Follow-up ticket for full process debt  

Still human-gated at each compressed step.
