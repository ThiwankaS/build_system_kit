# Example — export feature — component to-be

```mermaid
flowchart TB
  subgraph UI
    Page[Reports page]
    ExportBtn[Export control]
  end
  subgraph App
    Handler[Report handler]
    ExportAPI[Export endpoint]
  end
  subgraph Domain
    ReportSvc[Report service]
    ExportSvc[Export service]
  end
  subgraph Infra
    DB[(SQLite/DB)]
    Files[Object/files store]
  end
  Page --> Handler --> ReportSvc --> DB
  ExportBtn --> ExportAPI --> ExportSvc
  ExportSvc --> ReportSvc
  ExportSvc --> Files
```

## Delta (example)

- Changes: add Export control, endpoint, service, file store write
- Stays: existing report read path and DB ownership
- Risks: large-file timeouts; authz on export must match report ACLs
