# Installing the Agentic Build System kit into another repo

Target GitHub repository (publish pending SCM connect):

```text
https://github.com/ThiwankaS/build_system_kit.git
git@github.com:ThiwankaS/build_system_kit.git
```

Until the first push lands, copy from this Project’s `docs/agentic-build-system/` tree.

---

## Options

### 1. GitHub template repository (“Use this template”)

**Best for:** starting a **new** product repo that should *be* the build system (or a greenfield app that includes the kit as its process root).

1. On GitHub: mark the kit repo as a **Template repository**.
2. Click **Use this template** → create a new repo.
3. Clone; keep kit files at repo root (or move under `process/` / `.abs-kit/` if preferred).
4. Init context DB; start Intake.

| Pros | Cons |
|------|------|
| Clean history; no nested git metadata | Not for grafting into an *existing* product repo |
| Easy for greenfield | Upgrades are manual (re-copy or cherry-pick) |

---

### 2. `git subtree` add

**Best for:** existing product repos that want kit files **vendored in-tree** with a clear upgrade path.

```bash
# from product repo root
git remote add abs-kit https://github.com/ThiwankaS/build_system_kit.git
git fetch abs-kit
git subtree add --prefix=process/agentic-build-system abs-kit main --squash
```

Upgrade later:

```bash
git fetch abs-kit
git subtree pull --prefix=process/agentic-build-system abs-kit main --squash
```

| Pros | Cons |
|------|------|
| Files live in your repo (agents always see them) | Merge noise on upgrades |
| No submodule clone pitfalls | Prefix path must stay stable |

---

### 3. `git submodule`

**Best for:** many repos sharing one kit version pin; teams comfortable with submodules.

```bash
git submodule add https://github.com/ThiwankaS/build_system_kit.git process/agentic-build-system
git submodule update --init --recursive
```

Upgrade:

```bash
cd process/agentic-build-system && git fetch && git checkout <tag> && cd -
git add process/agentic-build-system && git commit -m "chore: bump build_system_kit"
```

| Pros | Cons |
|------|------|
| Clear version pin; small product history | Clone/CI must `--recurse-submodules` |
| Easy upstream tracking | Agents/humans forget to init submodules |

---

### 4. Sparse checkout / copy script

**Best for:** “bring process docs only” without full kit history, or monorepos that forbid submodules/subtrees.

Sparse clone then copy:

```bash
git clone --filter=blob:none --sparse https://github.com/ThiwankaS/build_system_kit.git /tmp/abs-kit
cd /tmp/abs-kit
git sparse-checkout set README.md USAGE.md INSTALL.md WORKFLOW.md feature-types.md \
  templates playbooks context adr diagrams .gitignore
# copy into product
mkdir -p /path/to/product/process/agentic-build-system
cp -a README.md USAGE.md INSTALL.md WORKFLOW.md feature-types.md \
  templates playbooks context adr diagrams .gitignore \
  /path/to/product/process/agentic-build-system/
```

Or a one-shot copy from a release tarball / this Project Context folder.

| Pros | Cons |
|------|------|
| Full control of what lands | No automatic upgrades |
| Works behind strict policies | Easy to drift from upstream |

---

## Recommended default for most teams

| Situation | Recommendation |
|-----------|----------------|
| **Existing product repo** | **`git subtree`** under `process/agentic-build-system/` |
| **Brand-new repo whose purpose is process + app** | **GitHub template** |
| **Many repos, strict version pins, submodule-fluent team** | **Submodule** |
| **Policy forbids nested remotes** | **Sparse / copy** |

**Default pick:** `git subtree` — kit files are always present for agents, upgrades are documented, and CI needs no special submodule flags.

### Suggested layout after install

```text
your-repo/
  process/agentic-build-system/   # kit (subtree/submodule/copy)
  .abs/
    context.db                    # gitignored binary (optional: commit empty via init)
  docs/                           # product docs (not the kit)
  ...
```

Add to product `.gitignore` (in addition to kit’s own):

```gitignore
.abs/context.db
.abs/context.db-*
.abs/*.db-wal
.abs/*.db-shm
```

Commit the kit’s `context/schema.sql` and CLI; do **not** commit WAL/SHM files.

---

## Upgrading the kit later

1. Read upstream `WORKFLOW.md` / changelog for breaking stage renames.
2. Subtree: `git subtree pull … --squash`. Submodule: bump pin. Template/copy: re-copy and diff.
3. Re-run `python3 process/agentic-build-system/context/abs_context.py init --db .abs/context.db` (idempotent schema).
4. Migrate any renamed template filenames; keep existing ADRs and approved artifacts.
5. Human approves “kit upgrade” as a chore stage (docs/chore feature type).

---

## Follow-up needed to publish

- Repo exists: `https://github.com/ThiwankaS/build_system_kit.git`
- **Blocked:** GitHub SCM access not yet connected to the agent environment — do not clone/push until connected.
- After connect: push `docs/agentic-build-system/` contents as the repo **root** → optionally mark as Template → verify install paths in this doc.
