# InfraFlow — Government Infrastructure Workflow & Project Monitoring Platform

> **Built for NHAI / PWD-style public infrastructure authorities** — managing the complete lifecycle of highway and civil infrastructure projects through a digital-first Government File system, configurable approval workflows, contractor billing pipelines, and real-time executive dashboards.

---

### 🌐 Live Demo & Important Notice

- **Frontend Application:** [https://infraflow-frontend.onrender.com](https://infraflow-frontend.onrender.com)
- **Backend API & Swagger:** [https://infraflow-backend-01ke.onrender.com/api/schema/swagger-ui/](https://infraflow-backend-01ke.onrender.com/api/schema/swagger-ui/)

> ⏳ **Note on Render Free Tier (Cold Starts):**  
> Because the backend is hosted on Render's free tier, the service automatically spins down after periods of inactivity. **The first request (such as logging in or fetching data) may take 50–60 seconds to wake up the server.** Once awake, all requests respond instantly.

---

## 🏛️ What is InfraFlow?

InfraFlow replaces paper note sheets, physical movement registers, and spreadsheet tracking with an integrated, role-based platform:
- **Contractors:** Upload documents, submit Running Account (RA) bills, raise Requests for Inspection (RFIs), and resolve Non-Conformance Reports (NCRs).
- **Authority Engineers:** Verify site measurements, inspect works, append note sheets, and forward files.
- **Finance & Executive Authorities (PD / RO):** Scrutinise invoices, sanction files, approve payments, and track portfolio SLAs.
- **Super Admin:** Centrally manage users, departments, custom workflows, SLA thresholds, and audit logs.

---

## 🔄 Lifecycle Flow: Contractor ⇄ Higher Authorities

InfraFlow implements strict **two-way (bidirectional)** government workflow protocols. Requests and documents move up the chain of command for sanction, and can be returned down the chain with remarks for clarification or rectification:

```
▲ UPWARD APPROVAL FLOW (Submission & Verification)
──────────────────────────────────────────────────────────────────────────────────
[Contractor]              [Authority Engineer]          [Finance / PD]            [Bank / PFMS]
     │                             │                           │                        │
     ├─ 1. Submits RA Bill / ─────►│                           │                        │
     │     RFI / Document          ├─ 2. Scrutiny & ──────────►│                        │
     │                             │     Measurement           ├─ 3. Financial Check    │
     │                             │     Verification          │     & Final Sanction   │
     │                             │     (Appends Note)        │     (Appends Note)     │
     │                             │                           │                        │
     │                             │                           ├─ 4. Issue Payment ────►│
     │                             │                           │    Sanction Order      │
──────────────────────────────────────────────────────────────────────────────────
▼ DOWNWARD RETURN FLOW (Objections, Clarifications & Resubmission)
──────────────────────────────────────────────────────────────────────────────────
[Contractor]              [Authority Engineer]          [Higher Authority]
     │                             │                           │
     │                             │◄── Returns with Query ────┤ (e.g., Budget Mismatch
     │                             │    or Objection           │  or Missing Drawing)
     │◄── Returns File / RFI ──────┤
     │    with Rectification Note  │
     │                             │
     ├─ Rectifies & Resubmits ────►│ (Resumes verification cycle)
```

### Flow Breakdown:
1. **Initiation (Contractor):** Contractor submits an RA bill, drawing, RFI, or variation order via the Contractor Portal. An official digital **Government File** is automatically created with an immutable tracking number.
2. **Technical Scrutiny (Authority Engineer):** The designated engineer visits the work site, checks quality and physical measurements against BOQ items, adds an official **Note Sheet**, and forwards the file upwards.
3. **Executive Approval & Sanction (Project Director / Regional Officer):** The Competent Authority reviews notes, verifies compliance against SLA timelines, and records an official sanction decision (**APPROVE**, **RETURN**, or **REJECT**).
4. **Return & Resubmission Loop:** If any discrepancy is found at any stage, the authority can **Return with Remarks**. The file rolls back to the previous desk or contractor with an objection note sheet. Once corrected, it is resubmitted along the same audit chain.
5. **Settlement & Audit:** Upon final approval, an automated disbursement advice is registered in the Payments log, and every action is sealed into an append-only, tamper-proof **Audit Trail**.

---

## 🔐 Demo User Credentials

All demo accounts share the password: **`DemoPass123!`**  
*(You can also click the quick 1-click login preset buttons on the Login page)*

| Role | Username | Primary Responsibilities |
|---|---|---|
| **System Super Admin** | `admin` | Full system control: users, org hierarchy, SLA rules, audit logs |
| **Project Director** | `project_director` | Approving authority: sanction bills, issue approvals, PIU oversight |
| **Authority Engineer** | `authority_engineer` | Site scrutiny: verify measurements, inspect quality, forward files |
| **Regional Officer** | `regional_officer` | Executive oversight: monitor regional bottlenecks & SLA escalations |
| **Contractor PM** | `contractor_pm` | Execution: submit RA bills, upload drawings, raise RFIs |

---

## 🛠️ Technology Stack

| Layer | Tech | Key Role |
|---|---|---|
| **Frontend** | React 18 + Vite | Fast single-page application with responsive light design |
| **Styling** | Tailwind CSS + Lucide Icons | Clean government-standard UI components and data tables |
| **Charts** | Recharts | Physical vs. financial progress analytics & SLA metrics |
| **Backend** | Django 5.0 + Django REST Framework | 18 domain-bounded modular apps with strict RBAC |
| **Security** | SimpleJWT | Stateless token authentication with request interceptors |
| **Database** | PostgreSQL | Relational storage for projects, bills, files, and audit records |
| **Static Hosting**| WhiteNoise + Gunicorn | Production-grade WSGI serving on cloud infrastructure |
| **Cloud Hosting**| Render | Automated multi-service deployment (Postgres + Django + React) |

---

## 🚀 Local Quickstart

### Prerequisites
- Python 3.11+
- Node.js 18+

### 1. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # On Windows (use: source venv/bin/activate on Linux/Mac)
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo     # Populates all demo users, projects, files & bills
python manage.py runserver 0.0.0.0:8000
```

### 2. Frontend Setup (in a separate terminal)
```bash
cd frontend
npm install
npm run dev
```

Visit **`http://localhost:5173`** to access the local portal.

---

## 📁 Core Repository Layout

```
├── backend/
│   ├── apps/
│   │   ├── accounts/          # User authentication & RBAC roles
│   │   ├── billing/           # RA bills, items, measurements & invoices
│   │   ├── files/             # Digital government files & note sheets
│   │   ├── projects/          # Projects, milestones, seed commands
│   │   ├── quality/           # RFIs, Site inspections, NCRs
│   │   ├── workflows/         # Approval steps & SLA escalation rules
│   │   └── audit/             # Immutable action logs
│   ├── config/                # Django project settings & URLs
│   └── build.sh               # Cloud build & migration script
├── frontend/
│   └── src/
│       ├── api/client.js      # Axios client with JWT auto-injection
│       ├── pages/             # Role portals: Admin, Work Desk, Contractor, etc.
│       └── components/        # Navigation bars, sidebars, badges, modals
├── render.yaml                # Render Blueprint deployment configuration
└── architecture.md            # In-depth architectural blueprint
```

---

## 📜 Disclaimer
*InfraFlow is a conceptual demonstration platform built for hackathon evaluation. Integration adapters (PFMS, e-Office, Aadhaar eSign) are mock implementations. All sample project data, bill numbers, and personnel names are fictional and intended solely for demo purposes.*
