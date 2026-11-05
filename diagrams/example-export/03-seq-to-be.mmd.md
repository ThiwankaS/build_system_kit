# Example — export feature — sequence to-be

```mermaid
sequenceDiagram
  actor U as User
  participant UI as Reports UI
  participant API as Export endpoint
  participant E as Export service
  participant S as Report service
  participant FS as Files
  U->>UI: Click export
  UI->>API: POST export
  API->>E: start job
  E->>S: load report
  S-->>E: data
  E->>FS: write file
  FS-->>E: uri
  E-->>API: ready
  API-->>UI: download link
  UI-->>U: Download
```

## Delta (example)

- Changes: async-capable export job + download link
- Stays: report load semantics and authz source of truth
- Risks: link expiry; PII in exported files
