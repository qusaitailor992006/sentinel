# Business Requirements Document (BRD)
## Project: SENTINEL — Enterprise Trust & Safety Intelligence Platform

---

### 1. Project Background
Digital marketplaces, fintech operators, and payment service providers face an accelerating surge in coordinated, automated fraud attacks, including:
- **Card Testing / Bin Attack Velocity**: Automated bots probing stolen credit card numbers using micro-transactions.
- **Account Takeover (ATO)**: Compromised credentials used to divert funds and buy high-liquidity goods (crypto, electronics).
- **Syndicates & Multi-Accounting**: Rings of coordinated entities sharing device fingerprints and VPN proxies to bypass merchant velocity caps.

Manual review queues are slow, expensive, and inconsistent, leading to elevated Mean Time to Detect (MTTD) and high False Positive Ratios (FPR) that damage legitimate customer relationships.

---

### 2. Business Objectives
1. **Reduce Fraud Loss**: Intercept high-risk anomalous transactions prior to financial settlement.
2. **Minimize False Positives**: Maintain an operational False Positive Ratio below 5.0% to preserve organic user conversion.
3. **Accelerate Investigation Velocity**: Reduce average investigation cycle time (MTTR) by at least 40% via automated AI forensic case dossiers.
4. **Enforce Regulatory Auditability**: Provide immutable audit logs tracking every status transition and enforcement action (Approve, Restrict, Ban) for regulatory compliance.

---

### 3. Stakeholder Profiles & Personas
- **Chief Risk Officer / VP of Trust & Safety**: Requires executive dashboards tracking aggregate loss exposure, FPR benchmarks, and policy efficiency.
- **Senior Fraud Lead**: Manages triage queue prioritization, handles escalations, and audits high-stakes enforcement decisions.
- **Risk Analyst / Investigator**: Investigates anomalous accounts, inspects entity graphs, reviews AI forensic summaries, and executes account actions.
- **Compliance / Internal Auditor**: Verifies adherence to KYC/AML and Fair Credit Reporting standards via immutable audit records.

---

### 4. Key Performance Indicators (KPIs)
- **Fraud Detection Rate (FDR)**: Percentage of fraudulent transactions successfully blocked.
- **False Positive Rate (FPR)**: Legitimate transactions erroneously flagged or blocked.
- **Mean Time to Resolve (MTTR)**: Average minutes spent by an analyst reviewing an alert.
- **Syndicate Resolution Ratio**: Number of multi-hop connected accounts neutralized per cluster detection.
