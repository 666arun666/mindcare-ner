# MINDCARE NER — Security Policy

## 1. Scope & Commitment
MINDCARE NER handles sensitive health interactions, cognitive session metrics, and caregiver data for elderly individuals. We take security, data privacy, and ethical AI operations with the utmost seriousness.

---

## 2. Secrets & Credentials Policy

### Absolute Rules
1. **Never Commit Secrets**: Never commit `.env` files, API keys, JWT secrets, database connection passwords, private keys (`.pem`, `.key`), or service account tokens into Git.
2. **Environment Variable Configuration**: All configuration must use environment variables (`.env.example` provides the documented template with placeholder values).
3. **CI/CD Secrets**: Production credentials, model endpoint keys (`OCR_LLM_TOKEN`), and deployment keys must only be stored in GitHub Repository Secrets.
4. **Untrusted PR Protection**: Pull requests from forks or untrusted branches are blocked from accessing production secrets.

---

## 3. Data Privacy & Healthcare Information (PHI/PII)

1. **No Sensitive Data in Logs**: Application code must never print or log patient names, phone numbers, addresses, auth tokens, or cognitive session transcripts to standard output or error logs.
2. **Device Pairing Security**: Elderly app devices authenticate via secure pairing tokens stored in device-encrypted keystores (`flutter_secure_storage` / Hive), never plain text.
3. **Caregiver Access Control**: Role-Based Access Control (RBAC) is enforced at the FastAPI router level. Caregivers are strictly isolated to their assigned patient records.
4. **Database Encryption**: Sensitive records must use encrypted columns where applicable, with TLS enforced for database connections in staging and production.

---

## 4. Automated Security Checks

Every pull request is automatically analyzed by `.github/workflows/security.yml`:
- **Gitleaks**: Scans commit history for secret patterns.
- **Bandit**: Static Application Security Testing (SAST) for Python code.
- **pip-audit**: Checks Python packages against the PyPA vulnerability advisory database.
- **npm audit**: Audits frontend JavaScript/TypeScript dependencies.
- **Hadolint**: Audits Docker container files for insecure practices.

---

## 5. Vulnerability Reporting

If you identify a security vulnerability in MINDCARE NER:
1. **Do not create a public GitHub issue.**
2. Report the vulnerability privately to the project maintainers:
   - Contact DevOps / Security Lead: `@TEAM_MEMBER_6`
   - Or email the security team (contact listed in repository settings).
3. Include:
   - Component affected (Backend, Dashboard, Elderly App, Voice, ML).
   - Detailed steps to reproduce the vulnerability.
   - Proof of Concept (PoC) if available.
4. The security team will acknowledge receipt within 48 hours and work on a coordinated fix via a private security advisory branch.
