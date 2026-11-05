# Stage 3 — Design

| Field | Value |
|-------|-------|
| Feature id | |
| Date | |

## As-is

```mermaid
flowchart TB
  subgraph today
    A[Module A] --> B[Module B]
  end
```

## To-be

```mermaid
flowchart TB
  subgraph proposed
    A[Module A] --> B[Module B]
    B --> C[Module C]
  end
```

## Delta caption (3–7 bullets)

- Changes:
- Stays:
- Risks:

## Contracts

| Interface / API / event | Shape / errors | Owner |
|-------------------------|----------------|-------|
| | | |

## Data shape (if any)

```mermaid
erDiagram
  ENTITY ||--o{ OTHER : has
```

## ADR updates

- [ ] None — fits confirmed ADRs
- [ ] New ADR: …
- [ ] Amend ADR-… (requires explicit human approve)

## Human approval

- [ ] **Approve** design (pair + delta + contracts)
- [ ] **Approve with notes:** …
- [ ] **Reject (fix in this stage):** …

Approver: ________  Date: ________
