# TA AI Project Scratchpad

## Active Tasks

### 1. MVP TA AI Q&A Assistant
- **Status**: Week 6 - Task 6.3 Monitoring & Logging In Progress; Task 7.1 CI/CD Complete; Task 7.2 Documentation In Progress; Task 7.3 Launch Checklist In Progress
- **Implementation Plan**: [MVP TA AI Implementation](./implementation-plan/mvp-ta-ai-qa-assistant.md)
- **Branch**: `feature/mvp-ta-ai-qa-assistant` ✅ Created
- **PR**: Not yet created
- **Planning Completed**: 2024-01-09
- **Development Started**: 2024-01-09
- **Week 1 Completed**: 2024-01-09
- **Weeks 2-5 Completed**: All core functionality implemented
- **Week 6 Task 6.1 Completed**: Security hardening (VNet, TLS, API auth, input validation)

## Lessons Learned

- [2024-01-09] On macOS ARM (Apple Silicon), `grpcio` package fails to build from source. Solution: Comment out Azure Functions dependencies temporarily and use plain FastAPI for local development. Azure packages can be installed in production/CI environment.
- [2025-08-08] OpenAI Python SDK breaking change: legacy embeddings usage removed. Use client-based `embeddings.create` with explicit model (e.g., `text-embedding-3-small`) or temporarily pin `openai==0.28.*`. Update code and tests.

## Project Overview

Building a single-course Q&A assistant for university courses that can:
- Ingest course materials (slides + lecture transcripts)
- Answer student questions 24/7 in professor's tone
- Provide exact citations from course materials
- Allow professor review and feedback

Target: ≤200 students, ≤1k questions/month, £80/$100 monthly budget
Timeline: 6 weeks for one engineer + part-time professor tester

## Key Planning Decisions

1. **Architecture**: Serverless Azure Functions with pgvector for cost optimization
2. **Tech Stack**: 
   - Frontend: Next.js with TypeScript
   - Backend: Python FastAPI on Azure Functions
   - LLM: GPT-4 Turbo via Azure OpenAI
   - Database: PostgreSQL with pgvector
3. **Security**: VNet with Private Endpoints to keep data within Azure
4. **Cost Strategy**: Pay-per-use model, estimated $65/month (well under budget)
5. **Development Approach**: 6-week sprint with weekly milestones, focusing on vertical slices 

## Planner Update (2025-08-08)

- Current focus: Production readiness. Embeddings API migration completed; query endpoint healthy locally; structured logging + request timing added; docs in progress.
- Detailed next steps and subtasks updated in `docs/implementation-plan/mvp-ta-ai-qa-assistant.md` (Planner Update and status board).

### Blockers
- None for local mock baseline. Azure activation pending credentials.

### Performance Testing Results (latest)
- Health endpoint: 42 GET, 0 failures (p95 ~10ms)
- Query endpoint: 222 POST, 0 failures (p95 ~10ms) — mock mode baseline
- Action taken: Migrated to client-based embeddings; added mock mode, structured logging + timing; updated tests.

### Prioritized Next Steps
1) Document Azure Monitor/Grafana setup; OTel exporter stub added (ENABLE_OTEL=1).
2) Complete deployment/ops/user docs; open a draft PR from `feature/mvp-ta-ai-qa-assistant` (tests green).
3) Azure activation when credentials available; apply Terraform and smoke test.