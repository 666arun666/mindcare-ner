# Contributing to MINDCARE NER

Welcome to the MINDCARE NER project! We are a 6-member student engineering team building an AI-based cognitive gaming and memory assistance platform for elderly dementia patients in the North Eastern Region of India (SIH26003).

To ensure production stability, clinical terminology compliance, and code quality, all contributors must follow this guide.

---

## 1. Development Workflow Overview

Our core engineering loop follows this strict lifecycle:

```
Developer
    │
    ▼
Feature Branch (branched from develop)
    │
    ▼
Pull Request (target: develop)
    │
    ▼
GitHub Actions CI + Security Checks
    │
    ▼
OpenCodeReview (AI-Assisted Insights)
    │
    ▼
Developer Addresses Findings
    │
    ▼
Human Review & Approval (Domain CODEOWNER)
    │
    ▼
Merge to develop
    │
    ▼
Release PR (develop → main)
    │
    ▼
Tagged Release on main (v0.1.0)
```

> [!IMPORTANT]
> - **NO DIRECT PUSHES TO `main` OR `develop`.**
> - **NO AUTOMATIC MERGE BY AI.** Alibaba OpenCodeReview provides suggestions, but approval by a human team member is mandatory.
> - **LANGCHAIN ONLY**: Never introduce or import `langgraph`.

---

## 2. Branching Conventions

Always branch from the latest `develop` branch:

```bash
# Update local develop
git checkout develop
git pull origin develop

# Create your feature/fix branch
git checkout -b feature/<descriptive-name>
# or
git checkout -b fix/<bug-description>
```

### Branch Naming Scheme
- `feature/<name>`: New features (e.g. `feature/memory-match-game`, `feature/adaptive-hint-scoring`)
- `fix/<name>`: Bug fixes (e.g. `fix/sqlite-sync-retry`, `fix/voice-stt-timeout`)
- `refactor/<name>`: Code restructuring without functional changes
- `docs/<name>`: Documentation improvements
- `hotfix/<name>`: Urgent production fixes branched directly from `main`

---

## 3. Pull Request Guidelines

1. **Keep PRs Focused**: One feature or bug fix per pull request.
2. **Fill Out the PR Template**: Ensure every section of `.github/pull_request_template.md` is completed:
   - Components changed.
   - Testing checklist (unit tests, manual testing).
   - Security & privacy checklist.
   - Medical/AI safety checklist (ensure no prohibited diagnostic claims).
   - Offline sync idempotency considerations.
3. **Ensure CI Passes**: All status checks in GitHub Actions (`ci / *`, `security / *`) must pass.
4. **Review OpenCodeReview Feedback**: Check the sticky comment posted by OpenCodeReview on your PR and resolve any high/critical security or safety flags.
5. **Request Human Review**: Tag the appropriate domain owner from `.github/CODEOWNERS`:
   - Member 1: Elderly App (`/apps/elderly_app/`)
   - Member 2: Caregiver Dashboard (`/apps/caregiver_dashboard/`)
   - Member 3: Backend & Database (`/backend/`, `/shared/contracts/`)
   - Member 4: AI/ML Engine (`/ml/`)
   - Member 5: Voice & Offline Sync (`/voice/`, `/shared/schemas/`)
   - Member 6: DevOps & Infrastructure (`/.github/`, `/docs/`, `/docker/`, `/scripts/`)

---

## 4. Local Development & Testing

Before opening a PR, always run formatting and tests locally:

### Backend
```bash
cd backend
pip install -e .
ruff check src/ tests/
ruff format --check src/ tests/
pytest -v tests/
```

### ML Engine
```bash
cd ml
pip install -e .
ruff check src/ tests/
ruff format --check src/ tests/
pytest -v tests/
```

### Voice Module
```bash
cd voice
pip install -e .
ruff check src/ tests/
pytest -v tests/
```

### Caregiver Dashboard (React)
```bash
cd apps/caregiver_dashboard
npm install
npm run lint
npx tsc --noEmit
npm test
npm run build
```

### Elderly App (Flutter)
```bash
cd apps/elderly_app
flutter pub get
dart format --output=none --set-exit-if-changed .
flutter analyze
flutter test
```

---

## 5. Medical Safety & Terminology Compliance

Because MINDCARE is an assistive and cognitive engagement platform:
- **NEVER** use diagnostic or clinical claims:
  - ❌ `"detects dementia"`, `"diagnoses Alzheimer's"`, `"cures dementia"`, `"predicts cognitive decline"`
- **ALWAYS** use assistive and observational terminology:
  - ✅ `"cognitive engagement"`, `"memory assistance"`, `"performance trend"`, `"unusual performance change"`
