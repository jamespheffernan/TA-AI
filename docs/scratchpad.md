# TA AI Project Scratchpad

## Active Tasks

### 1. MVP TA AI Q&A Assistant
- **Status**: Week 1 - Foundation & Infrastructure (Task 1.1 ✅ Completed)
- **Implementation Plan**: [MVP TA AI Implementation](./implementation-plan/mvp-ta-ai-qa-assistant.md)
- **Branch**: `feature/mvp-ta-ai-qa-assistant` ✅ Created
- **PR**: Not yet created
- **Planning Completed**: 2024-01-09
- **Development Started**: 2024-01-09

## Lessons Learned

- [2024-01-09] On macOS ARM (Apple Silicon), `grpcio` package fails to build from source. Solution: Comment out Azure Functions dependencies temporarily and use plain FastAPI for local development. Azure packages can be installed in production/CI environment.

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