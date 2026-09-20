# Architecture — InfraFlow

## Overview

InfraFlow follows a **Modular Monolith** architecture — 18 domain-bounded Django apps with strict internal separation, a single deployable unit, and a decoupled React frontend. This pattern balances domain clarity with operational simplicity for public infrastructure-scale workloads.

---

## High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                            USERS (Browser)                          │
│                                                                     │
│   ┌──────────────┐  ┌──────────────────┐  ┌─────────────────────┐  │
│   │  Govt Officer│  │  Contractor / PM │  │  Super Admin        │  │
│   │  (Work Desk) │  │  (Contractor     │  │  (Admin Portal)     │  │
│   │              │  │   Portal)        │  │                     │  │
│   └──────┬───────┘  └────────┬─────────┘  └──────────┬──────────┘  │
└──────────┼──────────────────┼────────────────────────┼─────────────┘
           │                  │                        │
           └──────────────────┴────────────────────────┘
                                     │ HTTPS
                     ┌───────────────▼───────────────┐
                     │      React Frontend App        │
                     │  Vite · React 18 · Router v6   │
                     │  Axios · Tailwind CSS · Lucide  │
                     │  Recharts · JWT LocalStorage    │
                     └───────────────┬───────────────┘
                                     │ REST API calls
                                     │ /api/v1/...
                     ┌───────────────▼───────────────┐
                     │      Django REST API Layer     │
                     │  DRF · SimpleJWT Auth          │
                     │  drf-spectacular (OpenAPI 3.0) │
                     │  django-cors-headers           │
                     │  Gunicorn (production WSGI)    │
                     └───────────────┬───────────────┘
                                     │
           ┌─────────────────────────▼──────────────────────────┐
           │              APPLICATION DOMAIN LAYER               │
           │                                                     │
           │  ┌───────────┐  ┌──────────────┐  ┌────────────┐  │
           │  │ accounts  │  │organizations │  │  projects  │  │
           │  │ contracts │  │    files     │  │ workflows  │  │
           │  │ documents │  │ monitoring   │  │  quality   │  │
           │  │  billing  │  │  payments    │  │   tasks    │  │
           │  │   audit   │  │notifications │  │  reports   │  │
           │  │  comms    │  │integrations  │  │            │  │
           │  └───────────┘  └──────────────┘  └────────────┘  │
           └─────────┬──────────────┬──────────────────────────┘
                     │              │
          ┌──────────▼──┐     ┌─────▼──────────────────┐
          │ PostgreSQL  │     │         Redis           │
          │ Primary DB  │     │  Message Broker + Cache │
          │ UUIDs/JSONB │     └─────────┬───────────────┘
          │ NUMERIC     │               │
          └─────────────┘     ┌─────────▼───────────────┐
                              │     Celery Workers       │
                              │  SLA Breach Checks       │
                              │  Email Notifications     │
                              │  Escalation Dispatch     │
                              └─────────────────────────┘
                     │
          ┌──────────▼──────────┐
          │   Object Storage    │
          │  Local FS (dev)     │
          │  S3-compatible (prod)│
          │  Documents, Drawings│
          └─────────────────────┘
```

---

## Frontend Architecture

```
src/
├── api/
│   └── client.js          ─── Axios instance (base URL, JWT interceptor)
│                              All API methods as named exports
│
├── context/
│   └── AuthContext.jsx    ─── Global auth state (user object, login/logout)
│                              JWT stored in localStorage
│                              Provides useAuth() hook to all components
│
├── components/
│   ├── Navbar.jsx         ─── Top bar (logo, org name, user name, logout)
│   └── Sidebar.jsx        ─── Role-aware navigation (govLinks / contractorLinks)
│
├── pages/
│   ├── Login.jsx              Login form + quick demo preset buttons
│   ├── AdminPanel.jsx         6-tab admin: Overview, Users, Orgs, Projects,
│   │                          Workflows, Audit Logs
│   ├── WorkDesk.jsx           Personalised file inbox + SLA metrics
│   ├── ExecutiveDashboard.jsx KPI cards + physical/financial progress bar chart
│   ├── ProjectList.jsx        Project cards with progress bars
│   ├── ProjectDetail.jsx      Project header + work packages table
│   ├── FileList.jsx           Government files repository table
│   ├── FileDetail.jsx         Note sheets, movement log, decisions
│   │                          + Forward / Approve modals
│   ├── BillsList.jsx          RA Bills table + submit new bill modal
│   ├── RFIsList.jsx           RFI inspection register
│   ├── NCRsList.jsx           Non-conformance report register
│   ├── ContractorDashboard.jsx Contractor KPI metrics + bill status tracker
│   ├── DocumentManager.jsx    Category-filtered doc grid + upload modal
│   └── (more pages as needed)
│
└── App.jsx                ─── Route definitions
                               ProtectedLayout (auth guard + Navbar + Sidebar)
                               Role-based default redirect on login
```

**Auth Flow:**
1. POST `/api/v1/auth/login/` → returns `access` + `refresh` JWT tokens
2. `access` stored in memory/localStorage, attached as `Authorization: Bearer <token>` header via Axios interceptor
3. `AuthContext` hydrates `user` object from token payload on page load
4. `ProtectedLayout` redirects to `/login` if no valid token

---

## Backend Domain App Architecture

Each app follows Django's MVT pattern with DRF ViewSets:

```
apps/<domain>/
├── models.py          Domain entities (inheriting from UUIDModel, TimestampModel)
├── serializers.py     DRF serializers (read/write, nested representations)
├── views.py           ViewSets (RBAC enforced in get_queryset / perform_create)
├── urls.py            Router registration
├── admin.py           Django Admin panel registration
├── signals.py         Post-save hooks (audit logging, notification dispatch)
└── management/
    └── commands/
        └── seed_demo.py   Creates all demo data (users, orgs, projects, files, bills)
```

### Domain Boundaries

| App | Responsibility |
|---|---|
| `accounts` | Custom User model, roles, designations, JWT authentication |
| `organizations` | Authority hierarchy — HQ → Regional Office → PIU → Contractor / Consultant |
| `projects` | Infrastructure project metadata, team assignments, BOQ |
| `contracts` | Contract documents, BOQ items, variation order tracking |
| `files` | `GovernmentFile` — central record container; `NoteSheet`, `Movement`, `Decision` |
| `workflows` | `WorkflowDefinition`, `WorkflowStep`, `WorkflowTransition`, `SLAPolicy`, `WorkflowInstance` |
| `documents` | `Document` metadata, `DocumentVersion`, `StorageService` abstraction |
| `communications` | Project correspondence, communication threads |
| `monitoring` | `WorkPackage`, progress percentages, milestone tracking |
| `quality` | `Inspection`, `RFI`, `NCR`, `ExtensionOfTime`, `ContractVariation` |
| `billing` | `Measurement`, `RABill`, 11-step bill workflow state machine |
| `payments` | Payment records, mock payment gateway adapter |
| `tasks` | Celery task definitions (SLA periodic checks, notification queue) |
| `audit` | Append-only `AuditLog` — actor, action, entity, timestamp, IP |
| `notifications` | In-app notification records + email dispatch via Django email backend |
| `reports` | Aggregation queries for Work Desk, Executive Dashboard, Contractor Dashboard |
| `integrations` | Mock adapters — PFMS, eOffice, eProcurement portal, eSign |

---

## Government File Lifecycle

```
                    ┌─────────────────────────────┐
                    │     GovernmentFile Created   │
                    │  (linked to RA Bill or issue)│
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │   Current Holder Receives    │
                    │   file on their Work Desk    │
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │  Officer writes Note Sheet   │
                    │  (observation / recommendation)│
                    └──────────────┬──────────────┘
                                   │
                ┌──────────────────┼──────────────────┐
                │ FORWARD          │ RETURN            │ APPROVE & SANCTION
                ▼                  ▼                   ▼
          Next Officer       Previous Holder      Decision recorded
          (Movement log      (Correction         (Append-only, immutable)
           updated)           required)
                │
                └──────► Repeat until competent authority
                          issues final APPROVAL / SANCTION
```

**Immutability Guarantee:** Note sheets and movement records are append-only. No record is ever deleted or modified after creation — full audit trail is preserved.

---

## SLA & Escalation Engine

```
File assigned to Officer
        │
        ├── t=0 ──────────► File appears on Work Desk
        │
        ├── t=warning_hours ► Badge turns AMBER (SLA Warning)
        │                     Email notification sent to officer
        │
        └── t=escalation_hours ► Badge turns RED (OVERDUE)
                                  Email escalated to supervisor role
                                  Celery periodic task updates is_overdue flag
                                  Executive Dashboard breach count incremented
```

Each `SLAPolicy` is configurable per workflow step:
- `warning_threshold_hours` — first nudge
- `escalation_threshold_hours` — hard breach, escalated to `escalation_target_role`

---

## RBAC Security Model

```
Request ──► JWT Validation ──► User.role extracted
                                      │
                    ┌─────────────────▼──────────────────┐
                    │       get_queryset() override        │
                    │  SUPER_ADMIN → all records          │
                    │  HQ_ADMIN    → all records          │
                    │  PROJECT_DIRECTOR → own PIU         │
                    │  AUTHORITY_ENGINEER → assigned files│
                    │  CONTRACTOR_* → own org's records   │
                    └─────────────────────────────────────┘
```

- No client-side trust — all scope enforcement is server-side in Django ViewSets
- Contractor users (`is_contractor_user=True`) are completely isolated from government records
- Super Admin (`is_superuser=True`) bypasses all scope filters

---

## Data Model Key Entities

```
Organization (tree: HQ → Regional → PIU → Contractor)
    │
    └── Project (code, location, contract value, progress %)
            │
            ├── WorkPackage (planned vs actual progress)
            │
            ├── GovernmentFile ◄── (linked to Bill or issue)
            │       ├── NoteSheet (append-only, author, recommendation)
            │       ├── Movement  (from_user → to_user, action, timestamp)
            │       └── Decision  (APPROVED / REJECTED, by authority, remarks)
            │
            ├── RABill (gross → deductions → net, 11-step status)
            │       └── linked GovernmentFile (bill processing file)
            │
            ├── Document (title, category, version, file path)
            │       └── DocumentVersion (version number, uploader, timestamp)
            │
            ├── RFI (location, description, inspection status)
            └── NCR (severity, specification breached, due date, status)
```