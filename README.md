# MINDCARE NER

[![CI](https://github.com/placeholder-org/mindcare-ner/actions/workflows/ci.yml/badge.svg)](https://github.com/placeholder-org/mindcare-ner/actions/workflows/ci.yml)
[![Security](https://github.com/placeholder-org/mindcare-ner/actions/workflows/security.yml/badge.svg)](https://github.com/placeholder-org/mindcare-ner/actions/workflows/security.yml)
[![OpenCodeReview](https://img.shields.io/badge/OpenCodeReview-Integrated-2ea44f)](https://github.com/alibaba/open-code-review)

**Smart India Hackathon (SIH 2026) — Problem Statement SIH26003**  
*Ministry of Development of North Eastern Region (DoNER)*  
**AI-Based Cognitive Gaming and Memory Assistance Platform for Elderly Dementia Patients in the North Eastern Region of India**

---

## 1. Project Overview

MINDCARE NER is an offline-first, voice-assisted, culturally localized cognitive support and memory assistance platform built for elderly users and their caregivers in North Eastern India.

### Key Capabilities
- **Offline-First Cognitive Gaming**: Tactile, high-contrast, large-button cognitive games that run entirely offline on Android devices.
- **Voice Assistance**: Ambient, allowlisted voice interaction powered by speech-to-text (STT) and text-to-speech (TTS) in regional languages.
- **Rule-Based Adaptive Difficulty**: Transparent, calibrated progression engine adjusting game difficulty based on accuracy, response speed, and hint utilization.
- **Idempotent Offline Synchronization**: Local SQLite storage queues immutable session events (`client_uuid`), automatically synchronizing to central PostgreSQL when internet connectivity is detected.
- **Caregiver Monitoring Dashboard**: Real-time engagement trends, medication reminders, and caregiver attention alerts.
- **Controlled LLM Orchestration**: Strictly powered by **LangChain** with sandboxed, allowlisted application tools.
- **Medical Safety by Design**: Focuses strictly on cognitive engagement and memory assistance — **never** presents diagnostic claims.

---

## 2. Monorepo Architecture & Directory Structure

```
mindcare-ner/
├── apps/
│   ├── elderly_app/              # Flutter/Dart mobile application (elderly UI, games, local SQLite/Hive)
│   └── caregiver_dashboard/      # React/TypeScript/Vite caregiver dashboard (charts, patient alerts)
├── backend/                      # FastAPI Python backend (Auth/RBAC, REST API, sync engine, Alembic)
├── ml/                           # Adaptive difficulty engine & Isolation Forest anomaly detector
├── voice/                        # Voice STT/TTS pipeline & allowlisted command validation
├── shared/
│   ├── schemas/                  # Shared Pydantic / JSON event models for offline sync
│   └── contracts/                # OpenAPI 3.1 specifications & API contracts
├── docs/
│   ├── architecture/             # CI/CD and system architecture documentation
│   ├── review/                   # MINDCARE code review rules & safety policies
│   └── decisions/                # Architectural Decision Records (ADRs)
├── docker/                       # Docker Compose and Dockerfile for containerized development
├── scripts/                      # Utility scripts (seed data, verification)
├── .github/
│   ├── workflows/                # CI, Security, and OpenCodeReview workflows
│   ├── CODEOWNERS                # 6-member team ownership mapping
│   ├── pull_request_template.md  # Standardized PR template
│   └── ISSUE_TEMPLATE/           # Bug, feature, and task issue templates
├── .opencodereview/
│   └── rule.json                 # Machine-readable OpenCodeReview rules
├── .gitignore
├── CONTRIBUTING.md               # Git workflow, PR lifecycle, and branch strategy
├── SECURITY.md                   # Secrets policy, PHI protection, vulnerability disclosure
└── README.md
```

---

## 3. Team Structure & Ownership (6 Members)

| Role | Domain / Directory | Responsibilities | Codeowner Handle |
|---|---|---|---|
| **Member 1** | `/apps/elderly_app/` | Flutter app, game engine, elderly UI/UX, local SQLite/Hive | `@TEAM_MEMBER_1` |
| **Member 2** | `/apps/caregiver_dashboard/` | React dashboard, charts, patient views, caregiver UI | `@TEAM_MEMBER_2` |
| **Member 3** | `/backend/`, `/shared/contracts/` | FastAPI services, PostgreSQL, Alembic migrations, Auth/RBAC | `@TEAM_MEMBER_3` |
| **Member 4** | `/ml/` | Adaptive difficulty engine, cold-start heuristics, Isolation Forest | `@TEAM_MEMBER_4` |
| **Member 5** | `/voice/`, `/shared/schemas/` | Voice STT/TTS, offline sync client, event schemas | `@TEAM_MEMBER_5` |
| **Member 6** | `/.github/`, `/docs/`, `/docker/`, `/scripts/` | DevOps, CI/CD, security policies, Docker, QA lead | `@TEAM_MEMBER_6` |

*Note: Replace `@TEAM_MEMBER_*` placeholders in `.github/CODEOWNERS` with actual GitHub usernames.*

---

## 4. Git & Branching Strategy

Our development process is designed for stability, continuous integration, and safety:

```
Developer
    │
    ▼
Feature Branch (feature/*, fix/*, refactor/*, docs/*)
    │
    ▼
Pull Request (target: develop)
    │
    ├─────────────────────┬─────────────────────┐
    ▼                     ▼                     ▼
GitHub Actions CI   Security Checks     OpenCodeReview
    │                     │                     │
    └─────────────────────┴─────────────────────┘
                          │
                          ▼
                 Human Code Review
             (CODEOWNER Sign-off Mandatory)
                          │
                          ▼
                  Merge to develop
                          │
                          ▼
                     Staging Test
                          │
                          ▼
                 Release PR (develop → main)
                          │
                          ▼
                        main
                   (Tagged v0.1.0)
```

- **No Direct Pushes to `main` or `develop`.**
- **Human Approval is Mandatory**: Alibaba OpenCodeReview assists developers by surfacing defects, but **only humans can approve and merge**.
- **No Automatic Code Changes by AI**: The AI reviewer never pushes code or merges PRs.

---

## 5. Local Development Setup

### Prerequisites
- Python 3.11+
- Node.js 20+ & npm
- Flutter SDK (for mobile app)
- Docker & Docker Compose

### 1. Clone the Repository
```bash
git clone https://github.com/placeholder-org/mindcare-ner.git
cd mindcare-ner
```

### 2. Infrastructure (PostgreSQL)
```bash
cp .env.example .env
docker compose -f docker/docker-compose.yml up -d
```

### 3. Backend (FastAPI)
```bash
cd backend
python -m venv .venv
# Activate virtual environment (.venv\Scripts\activate on Windows)
source .venv/bin/activate
pip install -e .
pytest -v tests/
uvicorn src.main:app --reload --port 8000
```

### 4. Caregiver Dashboard (React)
```bash
cd apps/caregiver_dashboard
npm install
npm run dev
```

### 5. Elderly App (Flutter)
```bash
cd apps/elderly_app
flutter pub get
flutter run
```

---

## 6. Testing Strategy

All pull requests must pass the automated test suites:
- **Backend**: API endpoints, JWT authentication, RBAC authorization, and sync idempotency (`pytest -v backend/tests`).
- **ML Engine**: Performance score formula, adaptive difficulty transitions, cold-start handling, and Isolation Forest anomaly interface (`pytest -v ml/tests`).
- **Voice Module**: Allowlisted command parsing and confirmation flows (`pytest -v voice/tests`).
- **Caregiver Dashboard**: TypeScript validation and unit tests (`npm test` in `apps/caregiver_dashboard`).
- **Elderly App**: Linter rules and widget tests (`flutter test` in `apps/elderly_app`).

Run all local Python tests at once:
```bash
python scripts/verify_all.py
```

---

## 7. Architecture & Review Rules

For full architectural blueprints, see:
- [CI/CD & Branching Architecture](docs/architecture/ci-cd.md)
- [Code Review & Safety Rules](docs/review/mindcare-review-rules.md)
- [ADR-001: GitHub Workflow](docs/decisions/ADR-001-github-workflow.md)
- [ADR-002: Strict LangChain LLM Orchestration](docs/decisions/ADR-002-langchain-orchestration.md)
