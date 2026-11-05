# Usage — apply this kit to any project

Works for **greenfield** (from scratch) and **brownfield** (existing codebase). Stack-agnostic: artifacts and checks, not frameworks.

---

## 0. Prerequisites

- Kit installed ([`INSTALL.md`](./INSTALL.md))
- Git + protected trunk (`main` / `trunk`)
- Python 3.9+ for the context CLI
- Humans available to Approve / Reject each stage

---

## 1. Initialize context cache

```bash
# from product repo root (adjust kit path)
KIT=process/agentic-build-system   # or wherever you installed it
mkdir -p .abs
python3 "$KIT/context/abs_context.py" init --db .abs/context.db
python3 "$KIT/context/abs_context.py" upsert-project --db .abs/context.db \
  --id my-app --name "My App" --dod "See WORKFLOW Definition of Done"
```

Agents must prefer `load-pack` over re-reading the whole repo.

---

## 2. Classify the change

Use [`feature-types.md`](./feature-types.md):

| Type | Branch prefix | Notes |
|------|---------------|-------|
| feature | `feature/<short-outcome>` | Full stage set (minus skips) |
| fix | `fix/<id>-<short>` | Usually skip UI polish if non-UI |
| chore | `chore/<short>` | Many stages optional |
| docs | `docs/<short>` | Docs-focused lane |
| hotfix | `hotfix/<short>` | Fast lane (still human-gated) |

Create the branch; register the feature:

```bash
python3 "$KIT/context/abs_context.py" upsert-feature --db .abs/context.db \
  --id F-123 --project my-app --branch feature/add-export --type feature \
  --status active --stage 0-intake
```

---

## 3. Brownfield first use (required once)

If the repo already has code and there is **no** approved architecture baseline:

1. Run stage **0b** — [`templates/00b-architecture-baseline.md`](./templates/00b-architecture-baseline.md)
2. Harvest ADRs into `adr/` + context `decisions` (status `inferred` until human confirms)
3. Human approves baseline → agents treat confirmed ADRs as **constraints**

Skip 0b only for true greenfield with nothing to respect.

```bash
python3 "$KIT/context/abs_context.py" load-pack --db .abs/context.db --feature F-123
```

---

## 4. Run stages (human gate each time)

For each **required** stage for the feature type:

1. **Agent** reads playbook `playbooks/<stage>.md` and `load-pack` output.
2. **Agent** fills `templates/<stage>.md` (copy into your feature workspace, e.g. `docs/features/F-123/`).
3. **Agent** produces ≤½ page summary + link to artifact.
4. **Human** replies: **Approve** | **Approve with notes** | **Reject (fix in this stage)**.
5. On approve: upsert artifact / diagrams / decisions; advance `current_stage`.
6. On reject: fix-forward in the **same** stage; do not skip ahead.

Never batch-approve remaining stages.

### Default delivery order (locked)

1. Design contracts (stage 3)  
2. Test design / failing specs (stage 6)  
3. Implementation (stage 7)  
4. UI polish (stage 5 polish after tests — flows may be sketched earlier in Design)

Threat review (stage 4): full notes when auth/data/network/PII change; otherwise a short “no new trust boundary” note.

---

## 5. Diagrams and ADRs

- Prefer Mermaid/PlantUML in templates; as-is + to-be + 3–7 bullet delta.
- Naming: see [`diagrams/NAMING.md`](./diagrams/NAMING.md).
- New architectural choices → new ADR from [`adr/TEMPLATE.md`](./adr/TEMPLATE.md); update [`adr/INDEX.md`](./adr/INDEX.md).
- Changing a confirmed ADR requires an amendment artifact + human approve.

---

## 6. Refactor documentation bar

If stage 9 runs, exit only when:

- Touched as-is/to-be diagrams updated or confirmed unchanged  
- Module overview / public contracts refreshed  
- ADR amended if boundaries changed  
- `doc_debt` cleared or explicitly deferred by human  

---

## 7. Done

Check Definition of Done in [`WORKFLOW.md`](./WORKFLOW.md). Update context DB; clean up branch per repo policy; run Retro (stage 15) so the next agent starts smarter.

---

## Agent read order (token budget)

1. `architecture_baseline` + `decisions` + `boundaries`  
2. Feature row + requirements / test_map  
3. Diagram pairs + latest approved artifacts  
4. Targeted files via `repo_index`  
5. Full-repo crawl only on cache miss or after large refactors  

---

## Hotfix fast lane

Still human-gated, compressed: problem + blast radius → failing regression test → minimal fix → review → deploy + verify → follow-up ticket for process debt. See [`feature-types.md`](./feature-types.md) and [`playbooks/hotfix.md`](./playbooks/hotfix.md).
