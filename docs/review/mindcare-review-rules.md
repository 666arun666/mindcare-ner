# MINDCARE NER — Code Review Guidelines & Safety Policy

**SIH26003: AI-Based Cognitive Gaming and Memory Assistance Platform for Elderly Dementia Patients in NER**  
*Applicable to both Human Reviewers and OpenCodeReview AI Reviewer.*

---

## 1. Core Review Principles

Every pull request in the MINDCARE NER monorepo must be evaluated against these domain-specific safety, privacy, and architecture rules. Reviewers (both AI and human) must enforce the following guidelines.

---

## 2. Rule Checklist & Standards

### 2.1 Medical Safety & Clinical Framing (CRITICAL)
- **NO Diagnostic Claims**: The platform is an offline-first cognitive engagement and memory assistance system, **NOT** a diagnostic tool.
- **Prohibited Words**: Flag any occurrences of:
  - `"detects dementia"`, `"diagnoses Alzheimer's"`, `"cures dementia"`, `"prevents dementia"`, `"predicts dementia"`, `"detects depression"`, `"measures mental health"`.
- **Mandatory Approved Terminology**:
  - Use `"cognitive engagement"`, `"memory assistance"`, `"personalized cognitive activities"`, `"performance trend"`, `"unusual performance change"`, `"caregiver attention flag"`.
- **Game Performance Framing**: Game scores represent task performance and engagement metrics only — never represent scores as a "cognitive health percentage" or dementia severity score.

### 2.2 LLM Orchestration & AI Safety (CRITICAL)
- **LangChain ONLY**: LangChain is the **only** approved LLM orchestration framework for MINDCARE NER.
- **DO NOT INTRODUCE LANGGRAPH**: Reject any PR that imports, installs, documents, or creates workflows with `langgraph`.
- **Controlled Tool Execution**: The LLM must never have direct, unrestricted access to the database or administrative services. All actions must flow through controlled, allowlisted application tools with schema-validated arguments.
- **Direct Database Writes Prohibited**: The LLM must not independently create or modify patient medical profiles, caregiver permissions, medications, or authentication records.

### 2.3 Anomaly Detection & Adaptive Difficulty (HIGH)
- **Isolation Forest Scoping**: Anomaly detection identifies *unusual patterns in game performance metrics*. The output must be formatted as:
  - `"Unusual performance change detected"` or `"Caregiver attention recommended"`.
  - Never describe anomaly outputs as `"Alzheimer's detected"` or `"Dementia onset"`.
- **Rule-Based Adaptive Difficulty**: The adaptive engine formula is:
  $$\text{performance\_score} = 0.5 \times \text{accuracy\_norm} + 0.3 \times \text{speed\_score} + 0.2 \times \text{hint\_efficiency}$$
  Ensure boundary conditions (0 hints, max hints, zero duration, missing values) are handled without crashing or division-by-zero.

### 2.4 Offline Synchronization & Idempotency (CRITICAL)
- **Client UUID**: Every session generated offline must carry a unique, client-generated UUID (`client_uuid`).
- **Idempotency Guarantee**: Server-side sync handlers (`/sync/upload`) must execute with idempotency (e.g. `ON CONFLICT (client_uuid) DO NOTHING`).
- **Retry Safety**: Re-transmitting an event batch after a network timeout or reconnect must never produce duplicate database entries.
- **State Machine Integrity**: Sessions move strictly from `PENDING` $\rightarrow$ `SYNCED` or `FAILED` (with retry schedule).

### 2.5 Security & Secret Management (CRITICAL)
- **No Hardcoded Secrets**: Zero tolerance for committed API keys, JWT secrets, passwords, database connection URIs, private keys, or `.env` files.
- **Authentication Validation**: Every protected backend endpoint must validate JWT access tokens or device-pairing tokens.
- **Authorization & RBAC**: Caregivers must not access patient data belonging to other caregivers. Patients must not access caregiver management APIs.
- **Safe Error Handling**: Exceptions and 500 error responses must never expose stack traces, database schema details, or system credentials to the client.

### 2.6 Data Privacy & Logging (HIGH)
- **No PHI/PII in Logs**: Patient names, contact details, notes, or cognitive session transcripts must not be written to application logs or console output in plain text.
- **Structured Redaction**: Use structured logging with automated redaction for sensitive fields.

### 2.7 Database Schema & Migrations (HIGH)
- **Versioned Migrations**: Any modification to SQLAlchemy models must be accompanied by an Alembic migration script.
- **No Silent Schema Drift**: Production schema changes must never be applied ad-hoc.
- **Foreign Key & Index Integrity**: Foreign keys (`patient_id`, `caregiver_id`) and unique constraints (`client_uuid`) must be explicitly defined.

### 2.8 Voice Processing & Intent Validation (MEDIUM)
- **Allowlisted Voice Commands**: The voice module must match against approved intent schemas (e.g. `"Start memory game"`, `"Remind me to drink water"`, `"What is my next activity?"`, `"Open today's game"`).
- **Confirmation Flow**: Any voice command triggering state changes (e.g. marking medication taken) requires explicit user confirmation.
- **Unrestricted Speech Rejection**: Voice input must not directly pass unvalidated natural language to system execution shells.

### 2.9 Elderly Usability & Localization (MEDIUM)
- **Accessibility**: Elderly UI components must adhere to high-contrast guidelines, large tap targets ($\ge 48 \times 48$ dp), clear typography, and voice prompt support.
- **Cultural Localization**: Regional North-Eastern cultural elements (themes, imagery, vernacular phrases) must be respectful, accurate, and avoid stereotypical or unsafe assumptions.

### 2.10 Testing Rigor (HIGH)
- New features require unit tests.
- Bug fixes require regression tests.
- Offline sync, adaptive engine formulas, and API routes must maintain high test coverage.

---

## 3. Severity Ratings for Findings

| Severity | Definition | Action Required |
|---|---|---|
| **CRITICAL** | Hardcoded secrets, diagnostic claims, LangGraph introduction, unauthenticated endpoints, sync data loss / duplicate corruption. | PR cannot merge. Must be remediated immediately. |
| **HIGH** | Missing RBAC checks, PHI in logs, missing database migrations, unhandled boundary conditions in adaptive engine. | Must be fixed before human approval. |
| **MEDIUM** | Missing unit tests for non-critical paths, suboptimal error responses, accessibility contrast issues. | Should be addressed or documented as tech debt. |
| **LOW / INFO** | Code style suggestions, minor refactorings, documentation typo fixes. | Non-blocking recommendations. |
