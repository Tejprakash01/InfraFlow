# InfraFlow — Government Infrastructure Workflow & Project Monitoring Platform

> **Built for NHAI / PWD-style public infrastructure authorities** — managing the complete lifecycle of highway and civil infrastructure projects through a digital-first Government File system, configurable approval workflows, contractor billing pipelines, and real-time executive dashboards.

---

## 🏛️ What is InfraFlow?

**InfraFlow** is a full-stack enterprise web platform that digitises the operational core of a Government Infrastructure Authority. It replaces paper-based file movement, manual RA bill processing, and siloed spreadsheet tracking with a unified, role-aware portal for:

- **Government Officers** — receive files, write note sheets, forward for approval, sanction bills
- **Project Directors** — oversee construction progress, review quality reports, approve payments
- **Contractors** — submit RA bills, upload drawings, request inspections (RFIs), close NCRs
- **Consultants** — review quality, certify measurements, raise non-conformance reports
- **Super Admin** — manage all users, organisations, workflows, SLAs, and audit trails

---

## 🚀 Key Features

| Domain | Features |
|---|---|
| **Government File Engine** | Immutable note sheets, movement history, parallel consultation, recommendations, approval & sanction |
| **Configurable Workflow Engine** | Data-driven multi-stage approval routes — sequential, parallel, monetary-threshold conditional routing, returns, SLA escalation |
| **Admin Portal** | Super Admin dashboard — user management, org hierarchy, workflow definitions, SLA rules, security audit logs |
| **Contractor Portal** | Submit RA bills, upload project documents (drawings, test reports, measurements), raise RFIs, close NCRs |
| **Digital RA Billing** | 11-step bill processing — contractor submission → document check → measurement verification → PD certification → finance scrutiny → authority approval → payment |
| **Quality & Compliance** | RFI register, Site Inspection verification, Non-Conformance Reports (NCRs), Extension of Time (EOT), Contract Variations |
| **Government Work Desk** | Personalised landing desk — pending files, SLA aging, overdue warnings, bottleneck tracking |
| **Executive Dashboard** | Portfolio KPIs, physical vs financial progress charts, SLA breach counts |
| **Document Repository** | Versioned DMS for contracts, engineering drawings, test certificates, measurement sheets, official correspondence |
| **Audit & Security** | Append-only tamper-proof audit trail, document versioning, server-side scope-based RBAC |

---

## 🛠️ Complete Technology Stack

### Backend

| Component | Technology | Version |
|---|---|---|
| Web Framework | **Django** | 5.0.x |
| REST API | **Django REST Framework (DRF)** | 3.14+ |
| Authentication | **SimpleJWT** (stateless JWT tokens) | 5.3.x |
| API Documentation | **drf-spectacular** (OpenAPI 3.0 / Swagger UI) | 0.27.x |
| Database ORM | Django ORM with PostgreSQL adapter | — |
| Database | **PostgreSQL** (UUIDs, NUMERIC, JSONB) | 16 |
| Async Task Queue | **Celery** | 5.3.x |
| Message Broker / Cache | **Redis** | 7 / 5.0.x |
| File Storage | **Pillow** + abstracted `StorageService` (local / S3-compatible) | 10.2.x |
| HTTP Client | **Requests** (integration adapters) | 2.31.x |
| CORS | **django-cors-headers** | 4.3.x |
| Production Server | **Gunicorn** (WSGI) | 21.2.x |
| Static Files | **WhiteNoise** | 6.6.x |
| DB URL Parsing | **dj-database-url** | 2.1.x |
| Env Management | **python-dotenv** | 1.0.x |

### Frontend

| Component | Technology | Version |
|---|---|---|
| UI Framework | **React** | 18.2.x |
| Build Tool | **Vite** | 5.1.x |
| Routing | **React Router DOM** | v6.22.x |
| HTTP Client | **Axios** | 1.6.x |
| UI Icons | **Lucide React** | 0.359.x |
| Charts | **Recharts** | 2.12.x |
| Styling | **Tailwind CSS** | 3.4.x |
| CSS Tooling | PostCSS + Autoprefixer | — |

### Infrastructure & Deployment

| Component | Technology |
|---|---|
| Containerisation | **Docker** + **Docker Compose** |
| Production Hosting | **Render** (render.yaml blueprint) |
| Database Hosting | Render Managed PostgreSQL |
| Dev Database | SQLite (local no-docker mode) |

---

## 🗂️ Repository Structure

```
Pravi hackathon/
├── backend/
│   ├── config/
│   │   ├── settings/
│   │   │   ├── base.py          # Shared settings (apps, middleware, auth, JWT)
│   │   │   ├── development.py   # SQLite, DEBUG=True, console email
│   │   │   └── production.py    # PostgreSQL, WhiteNoise, Redis, S3
│   │   ├── urls.py              # Root URL routing + API versioning (/api/v1/)
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── apps/
│   │   ├── accounts/            # Custom User model, JWT auth, role/designation
│   │   ├── organizations/       # Org hierarchy (HQ → Regional → PIU → Contractor)
│   │   ├── projects/            # Projects, team assignments, BOQ, seed_demo command
│   │   ├── contracts/           # Contract metadata, BOQ items, variation orders
│   │   ├── files/               # GovernmentFile, NoteSheet, Movement, Decisions
│   │   ├── workflows/           # WorkflowDefinition, Steps, Transitions, SLA policies
│   │   ├── documents/           # Document metadata, versioning, StorageService
│   │   ├── communications/      # Project correspondence and communication records
│   │   ├── monitoring/          # WorkPackages, progress %, milestones
│   │   ├── quality/             # Inspection, RFI, NCR, Variation, EOT
│   │   ├── billing/             # Measurements, RA Bills, 11-step bill workflow
│   │   ├── payments/            # Payment records, mock payment gateway adapter
│   │   ├── tasks/               # Celery task definitions (SLA checks, notifications)
│   │   ├── audit/               # Append-only AuditLog — immutable action records
│   │   ├── notifications/       # In-app notifications + email dispatch
│   │   ├── reports/             # Aggregation views (Executive Dashboard, Work Desk)
│   │   └── integrations/        # Mock adapters (PFMS, eOffice, eProcurement, eSign)
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── client.js        # Axios instance + all API method definitions
│   │   ├── components/
│   │   │   ├── Navbar.jsx       # Top navigation bar (light theme)
│   │   │   └── Sidebar.jsx      # Role-aware navigation sidebar
│   │   ├── context/
│   │   │   └── AuthContext.jsx  # JWT auth state, login/logout, user object
│   │   ├── pages/
│   │   │   ├── Login.jsx            # Login form + 1-click demo presets
│   │   │   ├── WorkDesk.jsx         # Government officer's file inbox
│   │   │   ├── ExecutiveDashboard.jsx # KPIs + Recharts progress chart
│   │   │   ├── ProjectList.jsx      # Infrastructure project cards
│   │   │   ├── ProjectDetail.jsx    # Project detail + work packages table
│   │   │   ├── FileList.jsx         # Government files repository
│   │   │   ├── FileDetail.jsx       # File detail — note sheets, movements, sanctions
│   │   │   ├── BillsList.jsx        # RA Bills table + submit new bill modal
│   │   │   ├── RFIsList.jsx         # Request For Inspection register
│   │   │   ├── NCRsList.jsx         # Non-Conformance Report register
│   │   │   ├── ContractorDashboard.jsx # Contractor metrics + bill tracker
│   │   │   ├── DocumentManager.jsx  # Document upload + versioned repository
│   │   │   └── AdminPanel.jsx       # Super Admin — 6-tab master control panel
│   │   ├── App.jsx              # Route definitions + protected layout wrapper
│   │   ├── main.jsx
│   │   └── index.css            # Tailwind directives + custom design tokens
│   ├── Dockerfile
│   ├── package.json
│   └── vite.config.js
│
├── docker-compose.yml           # Local stack: backend + frontend + postgres + redis
├── render.yaml                  # Render.com 1-click deployment blueprint
├── .env.example                 # Environment variables template
├── architecture.md              # High-level system architecture
└── README.md
```

---

## 🔐 User Roles & Demo Accounts

All demo accounts use the same password: **`DemoPass123!`**

| Username | Role | Portal | Access Level |
|---|---|---|---|
| `admin` | **SUPER_ADMIN** | Admin Portal | All users, orgs, workflows, audit logs |
| `project_director` | **PROJECT_DIRECTOR** | Work Desk | Approve bills, sanction files, manage PIU |
| `authority_engineer` | **AUTHORITY_ENGINEER** | Work Desk | Technical scrutiny, measurement verification |
| `regional_officer` | **REGIONAL_OFFICER** | Executive Dashboard | Regional SLA oversight, escalation management |
| `contractor_pm` | **CONTRACTOR_PROJECT_MANAGER** | Contractor Portal | Submit bills, upload documents, raise RFIs |

> Quick-login preset buttons are available directly on the Login page — no manual credential entry required for demos.

---

## ⚙️ Core Workflow — Government File & RA Bill Lifecycle

```
CONTRACTOR                    GOVERNMENT OFFICERS                    AUTHORITY
─────────                     ──────────────────                     ─────────

Submit RA Bill ─────────────► File Created (AUTO)
                               │
                               ▼
                         Authority Engineer
                         ├── Verify Measurements
                         ├── Write Note Sheet
                         └── Forward ──────────────────────────────► Finance Officer
                                                                       ├── Scrutinise Bill
                                                                       ├── Write Note Sheet
                                                                       └── Forward ────────► Project Director
                                                                                              ├── Review & Certify
                                                                                              ├── Write Note Sheet
                                                                                              └── APPROVE & SANCTION
                                                                                                   │
                                                                       Payment Record ◄────────────┘
                                                                       (PAID status)
```

### SLA Engine
- Each workflow step has configurable **warning** and **escalation** time thresholds
- Overdue files are flagged `OVERDUE` in the Work Desk and Executive Dashboard
- Celery background tasks run periodic SLA breach checks and dispatch notifications

---

## 💻 Local Development Setup

### Option A — Without Docker (Recommended for development)

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
cp ../.env.example .env
python manage.py migrate
python manage.py seed_demo     # Creates all demo users, projects, files, bills
python manage.py runserver 0.0.0.0:8000
```

**Frontend (separate terminal):**
```bash
cd frontend
npm install
npm run dev
```

Access at: **http://localhost:5173**

---

### Option B — Docker Compose (Full stack)

```bash
# Copy environment config
cp .env.example .env

# Build and launch all containers (backend + frontend + postgres + redis)
docker compose up --build

# In a separate terminal — run migrations and seed data
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py seed_demo
```

| Service | URL |
|---|---|
| Frontend App | http://localhost:5173 |
| Backend API | http://localhost:8000/api/v1/ |
| Swagger UI (API Docs) | http://localhost:8000/api/schema/swagger-ui/ |
| Health Check | http://localhost:8000/api/v1/health/ |
| Django Admin | http://localhost:8000/admin/ |

---

## 🌐 API Overview

All endpoints are versioned under `/api/v1/` and require JWT Bearer authentication except `/api/v1/auth/login/`.

| Endpoint Group | Path |
|---|---|
| Authentication | `/api/v1/auth/login/` · `/api/v1/auth/refresh/` |
| Users & Accounts | `/api/v1/users/` |
| Organizations | `/api/v1/organizations/` |
| Projects | `/api/v1/projects/` |
| Government Files | `/api/v1/files/` · `/api/v1/files/{id}/forward/` · `/api/v1/files/{id}/approve/` |
| RA Bills | `/api/v1/bills/` |
| Documents | `/api/v1/documents/` |
| RFIs | `/api/v1/rfis/` |
| NCRs | `/api/v1/ncrs/` |
| Workflows | `/api/v1/workflows/` |
| SLA Policies | `/api/v1/slas/` |
| Audit Logs | `/api/v1/audit/` |
| Notifications | `/api/v1/notifications/` |
| Dashboards | `/api/v1/reports/work-desk/` · `/api/v1/reports/executive/` · `/api/v1/reports/contractor/` |
| Health | `/api/v1/health/` |

Full interactive API documentation: **http://localhost:8000/api/schema/swagger-ui/**

---

## ☁️ Deployment on Render

The `render.yaml` blueprint provisions the full production stack on [Render.com](https://render.com) in one click:

1. Push repository to GitHub
2. Go to Render → **New Blueprint Instance** → select repo
3. Render automatically provisions:
   - **PostgreSQL Database** (managed, persistent)
   - **Django Web Service** (Gunicorn + WhiteNoise static files)
   - **React Static Site** (Vite production build via CDN)
4. Verify: `https://<your-backend>.onrender.com/api/v1/health/`

---

## 📜 Disclaimer

*InfraFlow is a conceptual demonstration platform. It is not legally equivalent to official Indian Government systems (e-Office, PFMS, eProcurement, GeM, Aadhaar eSign). All data is fictional and labeled as DEMO. Integration adapters are mock implementations.*
