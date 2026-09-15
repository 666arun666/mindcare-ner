## Description
<!-- Provide a brief explanation of what changed in this PR. -->

## Motivation
<!-- Why was this change required? What problem or feature does it address? -->

## Related Issue
<!-- Link the issue: e.g. Fixes #123, Closes #456 -->

---

## Components Changed
<!-- Check all components affected by this PR: -->
- [ ] Flutter (`apps/elderly_app`)
- [ ] React (`apps/caregiver_dashboard`)
- [ ] Backend (`backend`)
- [ ] ML (`ml`)
- [ ] Voice (`voice`)
- [ ] Offline Sync (`shared/schemas` / sync engine)
- [ ] Database (schema / Alembic migrations)
- [ ] API (endpoints / contracts)
- [ ] Documentation (`docs/`, `README.md`, etc.)
- [ ] CI/CD (`.github/workflows/`, Docker, scripts)

---

## Testing Checklist
- [ ] **Unit tests**: Added or updated unit tests and verified they pass locally.
- [ ] **Integration tests**: Verified end-to-end interactions where applicable.
- [ ] **Manual testing**: Verified user flows, edge cases, and error states manually.
- [ ] **Build validation**: Validated that build artifacts compile cleanly without warnings.

---

## Security Checklist
- [ ] **No secrets added**: Verified no API keys, tokens, passwords, `.env` files, or credentials are committed.
- [ ] **Authentication considered**: Protected endpoints verify valid JWTs / device tokens.
- [ ] **Authorization considered**: Role-based access control (RBAC) enforced (e.g., patient vs caregiver).
- [ ] **Sensitive data handling reviewed**: Passwords hashed, tokens secured in storage.

---

## Privacy Checklist
- [ ] **No unnecessary personal data**: Only required health/session metrics are collected.
- [ ] **No sensitive information in logs**: PHI and PII are redacted or omitted from stdout/stderr.
- [ ] **Data access is authorized**: Caregiver can only access patients assigned to them.

---

## AI/ML & Medical Safety Checklist
- [ ] **No unsupported medical claims**: Code, UI, and documentation DO NOT use prohibited diagnostic terms (*"detects dementia"*, *"diagnoses Alzheimer's"*, *"cures dementia"*, *"prevents dementia"*).
- [ ] **Approved terminology**: Uses *"cognitive engagement"*, *"memory assistance"*, *"performance trend"*, *"unusual performance change"*.
- [ ] **Model behavior tested**: Heuristics, boundary values (0 hints, max hints), and cold start validated.
- [ ] **Controlled LLM orchestration**: LLM calls strictly use **LangChain** and controlled allowlisted tools.
- [ ] **NO LangGraph**: Verified no imports, dependencies, or workflows of LangGraph exist.
- [ ] **No direct LLM DB writes**: LLM cannot directly modify database tables or sensitive records.

---

## Offline Synchronization Checklist
- [ ] **Offline behavior tested**: Local persistence (SQLite/Hive) functions seamlessly when disconnected.
- [ ] **Retry behavior tested**: Network failures trigger clean backoff/retry without data loss.
- [ ] **Duplicate sync behavior tested**: Server upserts are idempotent (`ON CONFLICT (client_uuid) DO NOTHING`); retries never create duplicate sessions.

---

## Breaking Changes
<!-- Describe any breaking changes to APIs, database schemas, environment variables, or configurations. If none, state "None". -->

---

## Screenshots / UI Previews
<!-- For Flutter or React changes, attach screenshots or short screen recordings. -->
