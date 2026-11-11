# SENTINEL: Enterprise Trust & Safety Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://react.dev/)
[![Scikit--Learn](https://img.shields.io/badge/Scikit--Learn-1.4-F7931E.svg)](https://scikit-learn.org/)
[![NetworkX](https://img.shields.io/badge/NetworkX-3.2-blueviolet.svg)](https://networkx.org/)
[![Groq LPU](https://img.shields.io/badge/Groq%20LPU-LLaMA%203.3%2070B-orange.svg)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

SENTINEL simulates the fraud detection, risk intelligence, and investigative case management lifecycle of high-volume digital platforms (e.g., Stripe Radar, PayPal Risk Engine, Airbnb Trust & Safety).

---

## Key Capabilities

- **Hybrid Risk Scoring**: Blends deterministic velocity thresholds with unsupervised Scikit-learn **Isolation Forest** anomaly detection.
- **Entity Resolution & Syndicate Detection**: Constructs multi-hop ego-networks via **NetworkX** to detect collusion rings sharing device fingerprints and proxy IP tokens.
- **AI Forensic Case Dossiers**: Integrates **GroqCloud LPUs (LLaMA 3.3 70B)** to synthesize raw telemetry into concise executive dossiers and recommended enforcement actions with sub-second latency.
- **Investigation Lifecycle & Case Management**: Dynamic triage queue with prioritization, case assignment, and immutable decision audit trails.
- **Executive BI Dashboard**: Monitors prevented fraud losses ($30K+), False Positive Ratios (FPR < 5%), and financial exposure across typologies.
- **Live Ingestion Simulator**: Interactive transaction injector to demonstrate real-time scoring and auto-triage live in interviews.

---

## System Architecture

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                            SENTINEL ARCHITECTURE FLOW                            │
│                                                                                  │
│   [Synthetic Data Generator] ──> [SQLAlchemy ORM + SQLite WAL / Postgres]        │
│                                             │                                    │
│   ┌─────────────────────────────────────────┴─────────────────────────────────┐  │
│   │                         SENTINEL INTELLIGENCE CORE                        │  │
│   │                                                                           │  │
│   │  [Heuristic Rules Engine]    [ML Anomaly Engine]      [NetworkX Graph]    │  │
│   │  - Velocity, Geolocation     - Isolation Forest       - Shared IP/Device  │  │
│   │  - Device Fingerprint Drift  - Scikit-Learn           - Collusion Rings   │  │
│   └─────────────────────────────────────────┬─────────────────────────────────┘  │
│                                             │                                    │
│                                    [Consolidated Risk Score]                     │
│                                             │                                    │
│       ┌─────────────────────────────────────┴──────────────────────────────┐     │
│       ▼                                                                    ▼     │
│  [Incident Triage & Case Workflow]                                    [Executive │
│  - React 18 + Tailwind Interface                                       Dashboard]│
│  - Groq LLaMA 3.3 Forensic Synthesis                                  - Loss KPI │
│  - Immutable Decision Audit Trail                                     - FPR / FDR│
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Start (Local Setup in 2 Minutes)

### Prerequisites
- Python 3.11+
- Node.js 18+

### 1. Clone Repository & Setup Backend
```bash
git clone https://github.com/your-username/sentinel.git
cd sentinel/backend

# Create virtual environment and install dependencies
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure Environment
Copy `.env.example` to `.env` in the root folder and add your free Groq API key:
```env
GROQ_API_KEY="your_groq_api_key_here"
```

### 3. Launch the Backend Server
```bash
python -m uvicorn backend.main:app --reload --port 8000
```
*The database automatically creates and seeds 600+ synthetic transactions and demo fraud rings upon startup at `http://127.0.0.1:8000/docs`.*

### 4. Launch the Frontend Application
In a second terminal:
```bash
cd sentinel/frontend
npm install
npm run dev
```
Open **`http://localhost:5173`** in your browser.

---

## Netlify Portfolio Deployment

A standalone, production-ready portfolio website is provided in `portfolio-site/`.

### 1-Click Netlify Drop Deployment:
1. Log in to [Netlify Drop](https://app.netlify.com/drop).
2. Drag and drop the `sentinel/portfolio-site/` folder directly onto the page.
3. Your live portfolio case study website will be instantly live with a public URL!

---

## Repository Structure

```
sentinel/
├── backend/
│   ├── app/
│   │   ├── api/            # REST Routers (cases, transactions, analytics, graph)
│   │   ├── core/           # Config, SQLite WAL database engine, security
│   │   ├── models/         # SQLAlchemy Relational Models (User, Account, Device, etc.)
│   │   ├── schemas/        # Pydantic validation schemas
│   │   └── services/       # ML Engine, NetworkX Graph, Groq Forensic Client, Synthetic Gen
│   ├── tests/              # Pytest automated test suites
│   ├── main.py             # FastAPI entrypoint
│   └── requirements.txt
├── frontend/
│   ├── src/                # React 18 + Tailwind components (Triage, Graph, BI, Simulator)
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── portfolio-site/         # 1-Click Netlify-ready portfolio showcase website
│   ├── index.html
│   └── _redirects
├── docs/                   # BRD, FRD, and 5-Minute Interview Demonstration Script
├── .env.example
├── .gitignore
└── README.md
```

---

## License
MIT License. Open-source enterprise portfolio platform.
