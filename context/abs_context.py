#!/usr/bin/env python3
"""Agentic Build System — minimal SQLite context CLI (stdlib only).

Usage examples:
  python3 abs_context.py init --db .abs/context.db
  python3 abs_context.py upsert-project --db .abs/context.db --id app --name "App"
  python3 abs_context.py upsert-feature --db .abs/context.db --id F-1 --project app --branch feature/x --type feature
  python3 abs_context.py upsert-decision --db .abs/context.db --id ADR-1 --project app --title "..." --status inferred
  python3 abs_context.py upsert-diagram --db .abs/context.db --id d1 --feature F-1 --role as-is --kind component --path docs/...
  python3 abs_context.py upsert-artifact --db .abs/context.db --id a1 --feature F-1 --stage 3-design --path docs/...
  python3 abs_context.py load-pack --db .abs/context.db --feature F-1
"""

from __future__ import annotations

import argparse
import hashlib
import os
import sqlite3
import sys
import uuid
from pathlib import Path
from typing import Any, Iterable, Optional


SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def connect(db: str) -> sqlite3.Connection:
    Path(db).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def cmd_init(args: argparse.Namespace) -> None:
    sql = SCHEMA_PATH.read_text(encoding="utf-8")
    with connect(args.db) as conn:
        conn.executescript(sql)
        conn.commit()
    print(f"initialized schema at {args.db}")


def _upsert(conn: sqlite3.Connection, table: str, key: str, key_val: str, fields: dict[str, Any]) -> None:
    cols = [key, *fields.keys()]
    placeholders = ", ".join("?" for _ in cols)
    updates = ", ".join(f"{c}=excluded.{c}" for c in fields.keys())
    # Touch updated_at when column exists
    if "updated_at" in _table_cols(conn, table):
        fields = {**fields, "updated_at": _now_sql()}
        # rebuild with updated_at
        cols = [key, *fields.keys()]
        placeholders = ", ".join("?" for _ in cols)
        updates = ", ".join(f"{c}=excluded.{c}" for c in fields.keys())
    sql = (
        f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({placeholders}) "
        f"ON CONFLICT({key}) DO UPDATE SET {updates}"
    )
    conn.execute(sql, [key_val, *fields.values()])


def _table_cols(conn: sqlite3.Connection, table: str) -> set[str]:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return {r["name"] for r in rows}


def _now_sql() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def _checksum(path: Optional[str]) -> Optional[str]:
    if not path or not os.path.isfile(path):
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def cmd_upsert_project(args: argparse.Namespace) -> None:
    with connect(args.db) as conn:
        _upsert(
            conn,
            "projects",
            "id",
            args.id,
            {
                "name": args.name,
                "stack_notes": args.stack_notes,
                "dod": args.dod,
            },
        )
        conn.commit()
    print(f"upserted project {args.id}")


def cmd_upsert_feature(args: argparse.Namespace) -> None:
    with connect(args.db) as conn:
        _upsert(
            conn,
            "features",
            "id",
            args.id,
            {
                "project_id": args.project,
                "branch": args.branch,
                "feature_type": args.type,
                "status": args.status,
                "current_stage": args.stage,
                "title": args.title,
            },
        )
        conn.commit()
    print(f"upserted feature {args.id}")


def cmd_upsert_decision(args: argparse.Namespace) -> None:
    with connect(args.db) as conn:
        _upsert(
            conn,
            "decisions",
            "id",
            args.id,
            {
                "project_id": args.project,
                "title": args.title,
                "context": args.context,
                "decision": args.decision,
                "consequences": args.consequences,
                "status": args.status,
                "diagram_refs": args.diagram_refs,
                "scope": args.scope,
            },
        )
        conn.commit()
    print(f"upserted decision {args.id}")


def cmd_upsert_baseline(args: argparse.Namespace) -> None:
    with connect(args.db) as conn:
        _upsert(
            conn,
            "architecture_baseline",
            "id",
            args.id,
            {
                "project_id": args.project,
                "version": args.version,
                "diagram_refs": args.diagram_refs,
                "approved_by": args.approved_by,
                "approved_at": args.approved_at or _now_sql(),
                "notes": args.notes,
            },
        )
        conn.commit()
    print(f"upserted baseline {args.id}")


def cmd_upsert_boundary(args: argparse.Namespace) -> None:
    bid = args.id or str(uuid.uuid4())
    with connect(args.db) as conn:
        _upsert(
            conn,
            "boundaries",
            "id",
            bid,
            {
                "project_id": args.project,
                "rule_text": args.rule,
                "status": args.status,
            },
        )
        conn.commit()
    print(f"upserted boundary {bid}")


def cmd_upsert_requirement(args: argparse.Namespace) -> None:
    with connect(args.db) as conn:
        _upsert(
            conn,
            "requirements",
            "id",
            args.id,
            {
                "feature_id": args.feature,
                "ac_text": args.text,
                "status": args.status,
            },
        )
        conn.commit()
    print(f"upserted requirement {args.id}")


def cmd_upsert_diagram(args: argparse.Namespace) -> None:
    with connect(args.db) as conn:
        _upsert(
            conn,
            "diagrams",
            "id",
            args.id,
            {
                "feature_id": args.feature,
                "project_id": args.project,
                "pair_role": args.role,
                "uml_kind": args.kind,
                "title": args.title,
                "path": args.path,
                "body": args.body,
            },
        )
        conn.commit()
    print(f"upserted diagram {args.id}")


def cmd_upsert_artifact(args: argparse.Namespace) -> None:
    checksum = args.checksum or _checksum(args.path)
    with connect(args.db) as conn:
        _upsert(
            conn,
            "artifacts",
            "id",
            args.id,
            {
                "feature_id": args.feature,
                "project_id": args.project,
                "stage": args.stage,
                "path": args.path,
                "checksum": checksum,
                "approved_by": args.approved_by,
                "approved_at": args.approved_at,
            },
        )
        conn.commit()
    print(f"upserted artifact {args.id}")


def cmd_upsert_test_map(args: argparse.Namespace) -> None:
    with connect(args.db) as conn:
        _upsert(
            conn,
            "test_map",
            "id",
            args.id,
            {
                "feature_id": args.feature,
                "ac_id": args.ac,
                "test_id": args.test,
                "file_path": args.file,
                "status": args.status,
            },
        )
        conn.commit()
    print(f"upserted test_map {args.id}")


def cmd_upsert_risk(args: argparse.Namespace) -> None:
    with connect(args.db) as conn:
        _upsert(
            conn,
            "risks",
            "id",
            args.id,
            {
                "feature_id": args.feature,
                "project_id": args.project,
                "description": args.description,
                "category": args.category,
                "mitigation": args.mitigation,
                "status": args.status,
            },
        )
        conn.commit()
    print(f"upserted risk {args.id}")


def cmd_upsert_repo_index(args: argparse.Namespace) -> None:
    with connect(args.db) as conn:
        _upsert(
            conn,
            "repo_index",
            "path",
            args.path,
            {
                "project_id": args.project,
                "purpose": args.purpose,
            },
        )
        conn.commit()
    print(f"upserted repo_index {args.path}")


def cmd_upsert_doc_debt(args: argparse.Namespace) -> None:
    with connect(args.db) as conn:
        _upsert(
            conn,
            "doc_debt",
            "id",
            args.id,
            {
                "project_id": args.project,
                "feature_id": args.feature,
                "area": args.area,
                "notes": args.notes,
                "status": args.status,
            },
        )
        conn.commit()
    print(f"upserted doc_debt {args.id}")


def _section(title: str, rows: Iterable[sqlite3.Row], cols: list[str]) -> str:
    lines = [f"## {title}", ""]
    rows = list(rows)
    if not rows:
        lines.append("(none)")
        lines.append("")
        return "\n".join(lines)
    for r in rows:
        parts = [f"{c}={r[c]}" for c in cols if c in r.keys() and r[c] is not None]
        lines.append("- " + " | ".join(parts))
    lines.append("")
    return "\n".join(lines)


def cmd_load_pack(args: argparse.Namespace) -> None:
    with connect(args.db) as conn:
        feat = conn.execute("SELECT * FROM features WHERE id=?", (args.feature,)).fetchone()
        if not feat:
            print(f"error: feature {args.feature} not found", file=sys.stderr)
            sys.exit(1)
        pid = feat["project_id"]
        out: list[str] = [
            f"# ABS load pack — feature {args.feature}",
            "",
            f"project={pid} branch={feat['branch']} type={feat['feature_type']} "
            f"status={feat['status']} stage={feat['current_stage']}",
            "",
            "Read order: baseline → decisions/boundaries → feature AC/tests → diagrams → artifacts → repo_index.",
            "",
        ]
        out.append(
            _section(
                "architecture_baseline",
                conn.execute(
                    "SELECT * FROM architecture_baseline WHERE project_id=? ORDER BY created_at DESC LIMIT 3",
                    (pid,),
                ),
                ["id", "version", "diagram_refs", "approved_by", "approved_at", "notes"],
            )
        )
        out.append(
            _section(
                "decisions",
                conn.execute(
                    "SELECT * FROM decisions WHERE project_id=? ORDER BY id",
                    (pid,),
                ),
                ["id", "title", "status", "scope", "diagram_refs"],
            )
        )
        out.append(
            _section(
                "boundaries",
                conn.execute(
                    "SELECT * FROM boundaries WHERE project_id=? ORDER BY id",
                    (pid,),
                ),
                ["id", "rule_text", "status"],
            )
        )
        out.append(
            _section(
                "requirements",
                conn.execute(
                    "SELECT * FROM requirements WHERE feature_id=? ORDER BY id",
                    (args.feature,),
                ),
                ["id", "status", "ac_text"],
            )
        )
        out.append(
            _section(
                "test_map",
                conn.execute(
                    "SELECT * FROM test_map WHERE feature_id=? ORDER BY id",
                    (args.feature,),
                ),
                ["id", "ac_id", "test_id", "file_path", "status"],
            )
        )
        out.append(
            _section(
                "diagrams",
                conn.execute(
                    "SELECT * FROM diagrams WHERE feature_id=? OR project_id=? ORDER BY pair_role, id",
                    (args.feature, pid),
                ),
                ["id", "pair_role", "uml_kind", "title", "path"],
            )
        )
        out.append(
            _section(
                "artifacts (latest)",
                conn.execute(
                    "SELECT * FROM artifacts WHERE feature_id=? ORDER BY created_at DESC LIMIT 20",
                    (args.feature,),
                ),
                ["id", "stage", "path", "approved_by", "approved_at"],
            )
        )
        out.append(
            _section(
                "risks",
                conn.execute(
                    "SELECT * FROM risks WHERE feature_id=? OR project_id=? ORDER BY id",
                    (args.feature, pid),
                ),
                ["id", "category", "status", "description", "mitigation"],
            )
        )
        out.append(
            _section(
                "doc_debt (open)",
                conn.execute(
                    "SELECT * FROM doc_debt WHERE project_id=? AND status!='cleared' ORDER BY id",
                    (pid,),
                ),
                ["id", "area", "status", "notes", "feature_id"],
            )
        )
        out.append(
            _section(
                "repo_index (sample)",
                conn.execute(
                    "SELECT * FROM repo_index WHERE project_id=? ORDER BY path LIMIT 50",
                    (pid,),
                ),
                ["path", "purpose"],
            )
        )
    print("\n".join(out))


def build_parser() -> argparse.ArgumentParser:
    # --db lives on a shared parent so `cmd --db PATH` works (not only `--db PATH cmd`).
    db_parent = argparse.ArgumentParser(add_help=False)
    db_parent.add_argument("--db", required=True, help="Path to SQLite DB file")

    p = argparse.ArgumentParser(description="ABS SQLite context CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_cmd(name: str, help: Optional[str] = None) -> argparse.ArgumentParser:
        return sub.add_parser(name, parents=[db_parent], help=help)

    s = add_cmd("init", help="Create/apply schema")
    s.set_defaults(func=cmd_init)

    s = add_cmd("upsert-project")
    s.add_argument("--id", required=True)
    s.add_argument("--name", required=True)
    s.add_argument("--stack-notes", default=None)
    s.add_argument("--dod", default=None)
    s.set_defaults(func=cmd_upsert_project)

    s = add_cmd("upsert-feature")
    s.add_argument("--id", required=True)
    s.add_argument("--project", required=True)
    s.add_argument("--branch", default=None)
    s.add_argument("--type", default="feature")
    s.add_argument("--status", default="active")
    s.add_argument("--stage", default="0-intake")
    s.add_argument("--title", default=None)
    s.set_defaults(func=cmd_upsert_feature)

    s = add_cmd("upsert-decision")
    s.add_argument("--id", required=True)
    s.add_argument("--project", required=True)
    s.add_argument("--title", required=True)
    s.add_argument("--context", default=None)
    s.add_argument("--decision", default=None)
    s.add_argument("--consequences", default=None)
    s.add_argument("--status", default="inferred", choices=["confirmed", "inferred", "superseded"])
    s.add_argument("--diagram-refs", default=None)
    s.add_argument("--scope", default=None)
    s.set_defaults(func=cmd_upsert_decision)

    s = add_cmd("upsert-baseline")
    s.add_argument("--id", required=True)
    s.add_argument("--project", required=True)
    s.add_argument("--version", required=True)
    s.add_argument("--diagram-refs", default=None)
    s.add_argument("--approved-by", default=None)
    s.add_argument("--approved-at", default=None)
    s.add_argument("--notes", default=None)
    s.set_defaults(func=cmd_upsert_baseline)

    s = add_cmd("upsert-boundary")
    s.add_argument("--id", default=None)
    s.add_argument("--project", required=True)
    s.add_argument("--rule", required=True)
    s.add_argument("--status", default="confirmed")
    s.set_defaults(func=cmd_upsert_boundary)

    s = add_cmd("upsert-requirement")
    s.add_argument("--id", required=True)
    s.add_argument("--feature", required=True)
    s.add_argument("--text", required=True)
    s.add_argument("--status", default="draft")
    s.set_defaults(func=cmd_upsert_requirement)

    s = add_cmd("upsert-diagram")
    s.add_argument("--id", required=True)
    s.add_argument("--feature", default=None)
    s.add_argument("--project", default=None)
    s.add_argument("--role", required=True, choices=["as-is", "to-be", "single"])
    s.add_argument("--kind", default="other")
    s.add_argument("--title", default=None)
    s.add_argument("--path", default=None)
    s.add_argument("--body", default=None)
    s.set_defaults(func=cmd_upsert_diagram)

    s = add_cmd("upsert-artifact")
    s.add_argument("--id", required=True)
    s.add_argument("--feature", default=None)
    s.add_argument("--project", default=None)
    s.add_argument("--stage", required=True)
    s.add_argument("--path", required=True)
    s.add_argument("--checksum", default=None)
    s.add_argument("--approved-by", default=None)
    s.add_argument("--approved-at", default=None)
    s.set_defaults(func=cmd_upsert_artifact)

    s = add_cmd("upsert-test-map")
    s.add_argument("--id", required=True)
    s.add_argument("--feature", required=True)
    s.add_argument("--ac", default=None)
    s.add_argument("--test", default=None)
    s.add_argument("--file", default=None)
    s.add_argument("--status", default="planned")
    s.set_defaults(func=cmd_upsert_test_map)

    s = add_cmd("upsert-risk")
    s.add_argument("--id", required=True)
    s.add_argument("--feature", default=None)
    s.add_argument("--project", default=None)
    s.add_argument("--description", required=True)
    s.add_argument("--category", default="threat")
    s.add_argument("--mitigation", default=None)
    s.add_argument("--status", default="open")
    s.set_defaults(func=cmd_upsert_risk)

    s = add_cmd("upsert-repo-index")
    s.add_argument("--path", required=True)
    s.add_argument("--project", required=True)
    s.add_argument("--purpose", required=True)
    s.set_defaults(func=cmd_upsert_repo_index)

    s = add_cmd("upsert-doc-debt")
    s.add_argument("--id", required=True)
    s.add_argument("--project", required=True)
    s.add_argument("--feature", default=None)
    s.add_argument("--area", required=True)
    s.add_argument("--notes", default=None)
    s.add_argument("--status", default="open", choices=["open", "cleared", "deferred"])
    s.set_defaults(func=cmd_upsert_doc_debt)

    s = add_cmd("load-pack", help="Print agent load pack for a feature")
    s.add_argument("--feature", required=True)
    s.set_defaults(func=cmd_load_pack)

    return p


def main(argv: Optional[list[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
