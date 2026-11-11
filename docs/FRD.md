# Functional Requirements Document (FRD)
## Project: SENTINEL — Enterprise Trust & Safety Platform

---

### 1. Data Ingestion & Storage Requirements
- **FR-1.1**: The platform shall store transaction and entity logs using an ORM layer (SQLAlchemy) compatible with local SQLite WAL mode and enterprise PostgreSQL.
- **FR-1.2**: Synthetic transaction generators shall produce realistic log-normal retail amounts alongside parameterized fraud typologies (Card Testing, ATO, Multi-Account Clusters).
- **FR-1.3**: The schema shall maintain distinct relational models for `Accounts`, `Devices`, `Transactions`, `Cases`, and `AuditLogs`.

---

### 2. Risk & Anomaly Intelligence Requirements
- **FR-2.1**: The system shall compute deterministic rule checks including 1-hour velocity spikes, foreign geolocation mismatches, and anonymous proxy detection.
- **FR-2.2**: The ML pipeline shall utilize Scikit-learn's `IsolationForest` to generate unsupervised anomaly divergence scores (0.0 to 1.0).
- **FR-2.3**: Composite risk scores (0 to 100) shall blend deterministic flags with ML anomaly outputs.
- **FR-2.4**: NetworkX shall construct multi-hop ego-networks up to 2 degrees to detect accounts sharing device hardware tokens.

---

### 3. AI Forensic Synthesis Requirements
- **FR-3.1**: The platform shall integrate with GroqCloud LPU inferencing using `llama-3.3-70b-versatile`.
- **FR-3.2**: If the 70B model encounters rate limits or errors, the service shall automatically fail over to `llama-3.1-8b-instant`.
- **FR-3.3**: Responses shall be strictly formatted as JSON objects containing:
  - `executive_summary`
  - `anomaly_breakdown`
  - `fraud_typology`
  - `recommended_action`
  - `confidence_score`
  - `justification`

---

### 4. Investigation & Audit Requirements
- **FR-4.1**: Investigators shall be able to filter cases by priority (`CRITICAL`, `HIGH`, `MEDIUM`) and status (`NEW`, `UNDER_REVIEW`, `RESOLVED`).
- **FR-4.2**: Enforcement actions (`BAN_ACCOUNT`, `RESTRICT_CARD`, `FLAG_FALSE_POSITIVE`) shall require written justification and generate append-only `AuditLog` entries.
