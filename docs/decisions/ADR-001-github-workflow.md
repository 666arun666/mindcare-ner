# ADR-001: GitHub Development Workflow, CI/CD, and OpenCodeReview Integration

## Context
MINDCARE NER is developed by a 6-member student engineering team for Smart India Hackathon 2026 (Problem Statement SIH26003). The team needs a collaborative, disciplined, and automated development workflow that protects production stability, enforces medical/clinical safety terminology, audits security, and ensures offline sync idempotency.

## Decision

1. **Monorepo Strategy**:
   The project is organized as a monorepo containing `apps/elderly_app` (Flutter), `apps/caregiver_dashboard` (React), `backend` (FastAPI), `ml` (Adaptive Engine & Anomaly Detection), `voice`, and `shared` schemas.

2. **Branching Model**:
   - `main`: Protected production branch. Direct pushes blocked.
   - `develop`: Protected integration branch. Direct pushes blocked.
   - Work happens exclusively on short-lived branches (`feature/*`, `fix/*`, `refactor/*`, `docs/*`).
   - Merging to `develop` requires automated CI passing and human approval.
   - Merging from `develop` to `main` happens through Release PRs.

3. **Multi-Job Path-Filtered CI**:
   GitHub Actions CI detects modified paths (`dorny/paths-filter`) to run only the relevant test suites (Flutter, React, FastAPI, ML, Voice), minimizing developer cycle time.

4. **Alibaba OpenCodeReview Integration**:
   - Integrated as an AI-assisted review step via `alibaba/open-code-review@main`.
   - Uses domain-specific rules configured in `.opencodereview/rule.json`.
   - **Crucial Guardrail**: OpenCodeReview is strictly advisory. It cannot merge PRs or push commits. Final approval authority rests solely with human team members.

5. **CODEOWNERS Mapping**:
   Six distinct functional roles map to directory ownership to ensure relevant domain leads review pull requests.

## Consequences
- Prevents accidental regressions and untested code in production.
- Ensures all team members adhere to code formatting, testing, and secret security standards.
- Accelerates peer review while maintaining human accountability.
