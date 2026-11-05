# Context cache (SQLite)

Stack-agnostic project memory for agents. **Python 3.9+**, stdlib `sqlite3` only — no pip install.

## Files

| File | Role |
|------|------|
| [`schema.sql`](./schema.sql) | Tables + indexes |
| [`abs_context.py`](./abs_context.py) | CLI: init, upserts, load-pack |

## Quick use

```bash
python3 context/abs_context.py init --db .abs/context.db
python3 context/abs_context.py upsert-project --db .abs/context.db --id demo --name "Demo"
python3 context/abs_context.py upsert-feature --db .abs/context.db \
  --id F-1 --project demo --branch feature/demo --type feature --stage 0-intake
python3 context/abs_context.py load-pack --db .abs/context.db --feature F-1
```

Do not commit `*.db` / WAL / SHM (see kit `.gitignore`). Commit schema + CLI.

## Agent contract

Before Design/Implementation on brownfield: run `load-pack` and honor baseline + decisions + boundaries.
