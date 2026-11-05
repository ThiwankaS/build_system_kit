# Diagram naming convention

## Files

```text
diagrams/<feature-or-area>/<stage>-<kind>-<role>.mmd.md
```

| Part | Values |
|------|--------|
| `feature-or-area` | feature id (`F-123`) or area slug (`auth`, `billing`) |
| `stage` | `00b`, `01`, `03`, `09`, … |
| `kind` | `seq` `cmp` `class` `state` `act` `er` `deploy` `flow` |
| `role` | `as-is` `to-be` `single` |

Examples:

- `diagrams/F-123/03-cmp-as-is.mmd.md`
- `diagrams/F-123/03-cmp-to-be.mmd.md`
- `diagrams/auth/00b-seq-as-is.mmd.md`

## Pairing

Always keep as-is / to-be as a **pair** with the same stage+kind prefix. Delta caption lives in the stage template (Design/Analysis/Refactor), not only in the diagram file.

## Context DB

`diagrams.id` should match a stable id such as `F-123-03-cmp-as-is`. Store `path` to the file; optional `body` for small inline snippets.
