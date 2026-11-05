# Stage 0b — Architecture baseline (brownfield)

| Field | Value |
|-------|-------|
| Repo / project id | |
| Baseline version | v1 |
| Date | |

## As-is — component / package

```mermaid
flowchart TB
  %% Replace with real modules
  UI[UI] --> App[App]
  App --> Domain[Domain]
  Domain --> Infra[Infra]
```

## As-is — key sequence

```mermaid
sequenceDiagram
  participant A as Actor
  participant S as System
  A->>S: request
  S-->>A: response
```

## Decision list (ADR harvest)

| ADR id | Summary | Status | Source |
|--------|---------|--------|--------|
| ADR-0001 | | inferred / confirmed / superseded | code / README / PR |

## Boundaries (allowed dependency directions)

```text
UI → App → Domain → Infra
```

Store in context `boundaries`.

## Doc debt spotted

| Area | Gap | Severity |
|------|-----|----------|
| | | |

## Human approval

Baseline becomes constraints for all later work until amended.

- [ ] **Approve** architecture baseline
- [ ] **Approve with notes:** …
- [ ] **Reject (fix in this stage):** …

Approver: ________  Date: ________
