-- Agentic Build System — SQLite context cache schema
-- Apply via: python3 abs_context.py init --db <path>

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS projects (
  id          TEXT PRIMARY KEY,
  name        TEXT NOT NULL,
  stack_notes TEXT,
  dod         TEXT,
  created_at  TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS features (
  id            TEXT PRIMARY KEY,
  project_id    TEXT NOT NULL REFERENCES projects(id),
  branch        TEXT,
  feature_type  TEXT, -- feature|fix|chore|docs|hotfix
  status        TEXT NOT NULL DEFAULT 'active',
  current_stage TEXT,
  title         TEXT,
  created_at    TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS decisions (
  id           TEXT PRIMARY KEY, -- e.g. ADR-0001
  project_id   TEXT NOT NULL REFERENCES projects(id),
  title        TEXT NOT NULL,
  context      TEXT,
  decision     TEXT,
  consequences TEXT,
  status       TEXT NOT NULL DEFAULT 'inferred', -- confirmed|inferred|superseded
  diagram_refs TEXT, -- comma-separated diagram ids or paths
  scope        TEXT,
  created_at   TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at   TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS architecture_baseline (
  id              TEXT PRIMARY KEY,
  project_id      TEXT NOT NULL REFERENCES projects(id),
  version         TEXT NOT NULL,
  diagram_refs    TEXT,
  approved_by     TEXT,
  approved_at     TEXT,
  notes           TEXT,
  created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS boundaries (
  id           TEXT PRIMARY KEY,
  project_id   TEXT NOT NULL REFERENCES projects(id),
  rule_text    TEXT NOT NULL,
  status       TEXT NOT NULL DEFAULT 'confirmed',
  created_at   TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at   TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS requirements (
  id          TEXT PRIMARY KEY,
  feature_id  TEXT NOT NULL REFERENCES features(id),
  ac_text     TEXT NOT NULL,
  status      TEXT NOT NULL DEFAULT 'draft',
  created_at  TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS artifacts (
  id           TEXT PRIMARY KEY,
  feature_id   TEXT REFERENCES features(id),
  project_id   TEXT REFERENCES projects(id),
  stage        TEXT NOT NULL,
  path         TEXT NOT NULL,
  checksum     TEXT,
  approved_by  TEXT,
  approved_at  TEXT,
  created_at   TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS diagrams (
  id          TEXT PRIMARY KEY,
  feature_id  TEXT REFERENCES features(id),
  project_id  TEXT REFERENCES projects(id),
  pair_role   TEXT NOT NULL, -- as-is|to-be|single
  uml_kind    TEXT, -- sequence|component|class|state|activity|er|deployment|other
  title       TEXT,
  path        TEXT,
  body        TEXT, -- optional inline mermaid/plantuml
  created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS test_map (
  id          TEXT PRIMARY KEY,
  feature_id  TEXT NOT NULL REFERENCES features(id),
  ac_id       TEXT,
  test_id     TEXT,
  file_path   TEXT,
  status      TEXT,
  created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS risks (
  id              TEXT PRIMARY KEY,
  feature_id      TEXT REFERENCES features(id),
  project_id      TEXT REFERENCES projects(id),
  description     TEXT NOT NULL,
  category        TEXT, -- threat|privacy|perf|other
  mitigation      TEXT,
  status          TEXT NOT NULL DEFAULT 'open',
  created_at      TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS repo_index (
  path         TEXT PRIMARY KEY,
  project_id   TEXT NOT NULL REFERENCES projects(id),
  purpose      TEXT,
  updated_at   TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS doc_debt (
  id          TEXT PRIMARY KEY,
  project_id  TEXT NOT NULL REFERENCES projects(id),
  feature_id  TEXT REFERENCES features(id),
  area        TEXT NOT NULL,
  notes       TEXT,
  status      TEXT NOT NULL DEFAULT 'open', -- open|cleared|deferred
  created_at  TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS run_log (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  feature_id      TEXT REFERENCES features(id),
  stage           TEXT,
  outcome         TEXT,
  token_estimate  INTEGER,
  notes           TEXT,
  created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_features_project ON features(project_id);
CREATE INDEX IF NOT EXISTS idx_decisions_project ON decisions(project_id);
CREATE INDEX IF NOT EXISTS idx_artifacts_feature ON artifacts(feature_id);
CREATE INDEX IF NOT EXISTS idx_diagrams_feature ON diagrams(feature_id);
CREATE INDEX IF NOT EXISTS idx_requirements_feature ON requirements(feature_id);
