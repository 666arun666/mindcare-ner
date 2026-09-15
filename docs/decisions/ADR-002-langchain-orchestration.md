# ADR-002: Strict LangChain LLM Orchestration and Explicit Exclusion of LangGraph

## Context
MINDCARE NER utilizes Large Language Models (LLMs) to provide conversational voice assistance, reminder formulation, and localized cognitive interactions for elderly dementia patients in the North Eastern Region of India.

Because this application serves a vulnerable demographic with cognitive impairment, safety and determinism are paramount:
- Autonomous, open-ended graph agents introduce non-deterministic execution paths, infinite loops, and debugging complexity that increase risk for elderly users.
- Direct database read/write access by LLMs creates risk of silent medical profile tampering or accidental caregiver permission escalation.

## Decision

1. **LangChain ONLY**:
   **LangChain is the sole approved LLM orchestration framework** for the MINDCARE NER platform.
2. **Explicit Prohibition of LangGraph**:
   - **DO NOT** install, import, document, or implement `langgraph`.
   - Any PR or dependency introducing LangGraph will be flagged as **CRITICAL** and immediately rejected.
3. **Controlled Tool Architecture**:
   The LLM is strictly decoupled from system state through an allowlisted tool architecture:
   ```
   User Voice / Touch
           │
           ▼
     Speech-to-Text
           │
           ▼
    Intent Extraction
           │
           ▼
   LangChain Orchestration
           │
           ▼
   Controlled Application Tool (Allowlisted Schema)
           │
           ▼
   Application Business Logic & Validation (Python/FastAPI)
           │
           ▼
   Database / Game Engine / Local Store
           │
           ▼
    Structured Response → TTS to User
   ```
4. **Sandboxed Data Operations**:
   - The LLM cannot directly modify patient profiles, caregiver permissions, medications, or authentication credentials.
   - All state mutations require verified application service authorization and explicit user or caregiver confirmation.

## Consequences
- Guaranteed deterministic behavior and simplified debugging during testing and SIH evaluation.
- Protection against unauthorized state changes.
- Eliminates dependency bloat and complex graph cycle states.
