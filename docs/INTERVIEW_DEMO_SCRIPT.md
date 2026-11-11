# 5-Minute Live Interview Demonstration Script
## Project: SENTINEL — Enterprise Trust & Safety Platform

---

### Phase 1: Context & Executive BI (0:00 - 1:00)
- **What to say**: 
  > *"SENTINEL is an enterprise Trust & Safety intelligence platform designed to simulate fraud operations at companies like Stripe and PayPal. In digital platforms, the primary operational challenge is balancing aggressive fraud interception against customer friction. If we open the Executive BI Dashboard, we see that SENTINEL has intercepted over $30,000 in simulated fraudulent volume while maintaining a False Positive Ratio under 5%."*
- **What to show**: 
  - Click on the **Executive BI** tab.
  - Highlight the 4 KPI cards: Prevented Fraud Loss, Scored Volume, False Positive Ratio, and Investigation Cycle Time.

---

### Phase 2: Incident Triage & ML Scoring (1:00 - 2:00)
- **What to say**: 
  > *"When transactions arrive, they are scored by a hybrid pipeline: deterministic velocity rules plus a Scikit-learn Isolation Forest anomaly detector. In the Incident Triage queue, incidents exceeding threshold are automatically prioritized into Critical, High, and Medium tiers so analysts focus on the most dangerous events first."*
- **What to show**: 
  - Switch to the **Incident Triage** tab.
  - Filter by `NEW` or `UNDER_REVIEW`.
  - Point out the composite **Risk Score (e.g. 94.2)** and the triggered rule flags.

---

### Phase 3: Entity Resolution & Syndicate Detection (2:00 - 3:00)
- **What to say**: 
  > *"One of the hardest fraud typologies to catch with standard rules is coordinated syndicates—where multiple accounts appear independent but share hardware fingerprints or VPN exit nodes. Let's inspect Case 2024-003."*
- **What to show**: 
  - Click on **Case-2024-003** (Syndicate Ring).
  - Inside the modal, switch to the **Fraud Network Graph** tab.
  - Point out the NetworkX ego-network showing 4 separate accounts co-operating across a single emulator device.

---

### Phase 4: Groq LLaMA 3.3 AI Forensic Synthesis (3:00 - 4:00)
- **What to say**: 
  > *"To reduce analyst investigation cycle time, I integrated GroqCloud LPUs running LLaMA 3.3 70B. Rather than forcing the analyst to read hundreds of raw log lines, the model synthesizes the anomaly signals, graph links, and transaction logs into an executive dossier with an evidence-based recommendation."*
- **What to show**: 
  - Click **"Run LLaMA 3.3 Analysis"**.
  - Show the live JSON synthesis returning an executive summary, anomaly breakdown, and recommended action (`BAN_ACCOUNT`).

---

### Phase 5: Enforcement, Audit Trail & Real-Time Simulator (4:00 - 5:00)
- **What to say**: 
  > *"To ensure regulatory compliance, any action taken by an investigator must be auditable. When I click 'Ban Account & Entities', an immutable record is logged. Furthermore, using our Live Simulator, we can inject a brand new transaction in real-time and watch the engine intercept it live."*
- **What to show**: 
  - Click **"Ban Account & Entities"**, enter an audit justification note, and show the updated status.
  - Switch to the **Audit Trail** tab to show the recorded timestamp and action.
  - (Bonus) Open the **Live Fraud Simulator** tab, click "Inject & Score Transaction Live", and see the real-time scoring.
