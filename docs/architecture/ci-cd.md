# MINDCARE NER — CI/CD & GitHub Workflow Architecture

**Project**: SIH26003 — AI-Based Cognitive Gaming & Memory Assistance Platform for Elderly Dementia Patients in NER  
**Target Audience**: 6-Member Student Engineering Team, Mentors, Evaluators

---

## 1. Overview & Core Philosophy

The MINDCARE NER engineering workflow is built for an offline-first, safety-critical healthcare platform developed by a 6-member student team. The pipeline ensures:
1. **High velocity with zero regression**: Independent components (Flutter, React, FastAPI, ML, Voice) run targeted CI pipelines.
2. **Medical & Terminology Safety**: Diagnostic claims are strictly banned across code and PRs; only approved assistive terminology is permitted.
3. **Strict LLM Orchestration**: **LangChain** is the sole approved LLM orchestration framework.
4. **Offline Sync Idempotency**: Offline session events with `client_uuid` are verified against duplicate server writes.
5. **AI Review with Human Primacy**: Alibaba OpenCodeReview provides automated, line-level feedback, but **Human approval is mandatory for all merges**.

---

## 2. End-to-End Workflow Diagram

```
Developer
    │
    ▼
Feature Branch (feature/*, fix/*)
    │
    ▼
Pull Request (Target: develop)
    │
    ├─────────────────────────────┬─────────────────────────────┐
    ▼                             ▼                             ▼
GitHub Actions CI           Security Checks             OpenCodeReview
├── Path Change Detection   ├── Gitleaks Secret Scan    ├── Rule Engine
├── Flutter Test & Analyze  ├── Bandit Python SAST       ├── Sticky PR Summary
├── React Lint, Types, Build ├── pip-audit & npm audit   └── Advisory Findings
├── FastAPI Test & Cov      └── Hadolint Container
├── ML Boundary Tests
└── Voice Intent Tests
    │                             │                             │
    └─────────────────────────────┴─────────────────────────────┘
                                  │
                                  ▼
                            Human Review
                    (Domain Owner from CODEOWNERS)
                                  │
                                  ▼
                              Approval
                                  │
                                  ▼
                           Merge to develop
                         (Integration Branch)
                                  │
                                  ▼
                         Staging Verification
                        (Docker Compose / E2E)
                                  │
                                  ▼
                        Release Pull Request
                                  │
                                  ▼
                                 main
                         (Production & Demo)
                                  │
                                  ▼
                             Tag (v0.1.0)
```

---

## 3. Branching Strategy

| Branch | Purpose | Protection Rules | Permitted Merges |
|---|---|---|---|
| `main` | Production & Demo state. Stable, tested, release-tagged. | Strict: Direct push blocked, PR required, $\ge 1$ approvals, all CI green. | Only via Release PR from `develop` or emergency `hotfix/*`. |
| `develop` | Integration branch. Active development convergence. | PR required, CI must pass, $\ge 1$ domain human review. | Feature branches (`feature/*`), bug fixes (`fix/*`), refactors (`refactor/*`). |
| `feature/<name>` | New capabilities developed by team members. | None. Developer owned. | Merges into `develop` via PR. |
| `fix/<name>` | Non-urgent bug fixes. | None. Developer owned. | Merges into `develop` via PR. |
| `hotfix/<name>` | Urgent production bug fixes. | None. Fast-tracked PR. | Merges into `main` AND back-merged into `develop`. |
| `refactor/<name>`| Code modernization without feature changes. | None. | Merges into `develop`. |
| `docs/<name>` | Documentation updates. | None. | Merges into `develop`. |

---

## 4. Continuous Integration (CI) Architecture

Our CI workflow (`.github/workflows/ci.yml`) is divided into distinct jobs that execute in parallel, triggered conditionally using `dorny/paths-filter` to minimize wait times:

### 4.1 Flutter Elderly App CI (`apps/elderly_app/**`)
- Restores Flutter packages via `flutter pub get`.
- Verifies code formatting with `dart format --output=none --set-exit-if-changed .`.
- Runs static analysis: `flutter analyze` (enforces strict linter rules).
- Executes unit and widget tests: `flutter test --coverage`.

### 4.2 React Caregiver Dashboard CI (`apps/caregiver_dashboard/**`)
- Uses Node.js 20 with `npm ci` caching.
- Enforces code quality: `npm run lint`.
- Validates strict typing: `npx tsc --noEmit`.
- Runs component tests: `npm test`.
- Compiles production bundle: `npm run build`.

### 4.3 FastAPI Backend CI (`backend/**`, `shared/**`)
- Python 3.11 environment.
- Code style and format: `ruff check` and `ruff format --check`.
- Test suite: `pytest -v --cov=src tests/`.
- Validates:
  - JWT authentication & device pairing token verification.
  - Role-Based Access Control (RBAC) dependencies.
  - Idempotent `/sync/upload` endpoint using client UUIDs.

### 4.4 AI/ML Engine CI (`ml/**`)
- Validates rule-based adaptive engine calculation:
  $$\text{performance\_score} = 0.5 \times \text{accuracy\_norm} + 0.3 \times \text{speed\_score} + 0.2 \times \text{hint\_efficiency}$$
- Cold start and boundary tests (0 hints, maximum hints, zero reaction time, missing values).
- Isolation Forest anomaly detection interface (verifying output is `"Unusual performance change"`, never diagnostic).

### 4.5 Voice Processing CI (`voice/**`)
- Validates speech intent parsing against allowlisted commands:
  - `"Start memory game"`
  - `"Remind me to drink water"`
  - `"What is my next activity?"`
  - `"Open today's game"`
- Confirms state changes require user confirmation.
- Rejects unallowlisted or arbitrary speech inputs.

---

## 5. Security & Secret Management

Security pipeline (`.github/workflows/security.yml`):
- **Gitleaks**: Scans commit history and PR diffs to prevent secrets, tokens, and private keys from entering git history.
- **Python SAST & Audit**: Bandit checks for common security anti-patterns (e.g. `eval`, insecure temp files), while `pip-audit` flags vulnerabilities in third-party Python packages.
- **Node Audit**: `npm audit --audit-level=high` checks frontend dependency supply chain security.
- **Docker Security**: Hadolint enforces container best practices (no root user, pinned tags).

---

## 6. OpenCodeReview & Human Review Interaction

Alibaba OpenCodeReview runs automatically on every pull request targeting `main` or `develop`.

### 6.1 Role of OpenCodeReview
- Serves as an **AI-assisted code reviewer**.
- Inspects PR diffs against `.opencodereview/rule.json` and `docs/review/mindcare-review-rules.md`.
- Posts actionable comments with line-level precision and a sticky summary.

### 6.2 The Safety Guardrail
```
AI Reviews PR
     │
     ▼
AI Reports Findings (CRITICAL / HIGH / MEDIUM / LOW / INFO)
     │
     ▼
Developer Addresses Feedback & Commits Fixes
     │
     ▼
CI Pipeline Re-runs Automatically
     │
     ▼
Human Code Owner Reviews PR
     │
     ▼
Human Approves and Merges
```
> [!IMPORTANT]
> **OpenCodeReview has ZERO merge authority**. It cannot approve PRs, merge code, or push commits to developer branches.

---

## 7. Release & Deployment Process (CD)

For SIH prototype and pilot delivery, we follow a simple, robust release flow without overengineering:

1. **Sprint Convergence on `develop`**:
   All peer-reviewed and tested features merge into `develop`.
2. **Staging Validation**:
   Spin up integration environment using `docker-compose up`:
   - Backend + PostgreSQL.
   - Verify offline sync end-to-end with Flutter and React builds.
3. **Release PR**:
   Create a PR from `develop` $\rightarrow$ `main` titled `Release v0.1.0`.
4. **Approval & Tagging**:
   - Member 6 (DevOps Lead) and domain leads perform final sign-off.
   - PR is merged into `main`.
   - Git tag created:
     ```bash
     git tag -a v0.1.0 -m "Release v0.1.0 - SIH MVP Prototype"
     git push origin v0.1.0
     ```
5. **Demo Deployment**:
   - Backend runs via Docker Compose on demo host / cloud VM.
   - React dashboard served via static hosting or Nginx container.
   - Flutter elderly app APK distributed for Android tablet/phone testing.
