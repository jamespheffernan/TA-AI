# TA AI - Q&A Assistant for University Courses

A cost-effective, privacy-first Q&A assistant that helps university courses provide 24/7 student support while maintaining the professor's tone and citing exact sources.

## Features

- **Course Material Ingestion**: Process slides (PDF/PPTX) and lecture transcripts
- **Intelligent Q&A**: Answer student questions using professor's tone with exact citations
- **Professor Oversight**: Review logs, flag incorrect answers, maintain quality control
- **Privacy & Security**: All data stays within Azure region using Private Endpoints
- **Cost Optimized**: Serverless architecture targeting <£80/month for 200 students

## Architecture

```
┌──────────┐   upload   ┌──────────────┐     chunk/     ┌────────────┐
│Professor │──────────►│Ingestion Fn  │──embed + store►│Postgres +  │
│Portal    │           │(Azure Fn)    │                │pgvector DB │
└──────────┘           └──────────────┘                └────────────┘
                                         query
     SSO (OIDC)                        ┌───────────┐   top-k vectors
Student  ───► Next.js chat ► API Fn ──►│GPT-4 Turbo│◄──(Azure OpenAI)  
browser     (Azure Fn, private VNet)   └───────────┘      (UK South PE)
                                   ↑    citations
                      log Q&A in Postgres; expose to prof dashboard
```

## Technology Stack

- **Frontend**: Next.js 14 with TypeScript, Tailwind CSS
- **Backend**: Python 3.11 with FastAPI on Azure Functions
- **Database**: PostgreSQL 15 with pgvector extension
- **LLM**: GPT-4 Turbo via Azure OpenAI Service
- **Embeddings**: text-embedding-3-small
- **Auth**: Microsoft Entra ID (OIDC)
- **Infrastructure**: Azure (Functions, Static Web Apps, VNet, Private Endpoints)
- **IaC**: Terraform

## Project Structure

```
├── frontend/          # Next.js application
├── backend/           # Python Azure Functions
├── infrastructure/    # Terraform modules
├── docs/             # Documentation and planning
└── tests/            # Test suites
```

## Development Timeline

- **Week 1**: Foundation & Infrastructure
- **Week 2**: Data Ingestion Pipeline  
- **Week 3**: Query & Retrieval System
- **Week 4**: Frontend Development
- **Week 5**: Professor Dashboard
- **Week 6**: Production Readiness

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.11+
- Azure CLI
- Terraform
- PostgreSQL with pgvector

### Local Development

```bash
# Clone repository
git clone <repo-url>
cd ta-ai

# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies
cd ../backend
pip install -r requirements.txt

# Set up infrastructure
cd ../infrastructure
terraform init
terraform plan
```

## Cost Estimation

| Component | Monthly Cost |
|-----------|--------------|
| GPT-4 Turbo tokens | $32 |
| Embeddings | $1 |
| Azure Postgres | $25 |
| Azure Functions | $2 |
| Static Web App | $0 |
| Misc | $5 |
| **Total** | **$65** |

## Security

- All resources within Azure VNet
- Private Endpoints for OpenAI API
- Encrypted storage and backups
- 30-day log retention
- SSO authentication via Microsoft Entra

## License

MIT License - see LICENSE file for details.

## Support

For questions or issues, please see the documentation in the `docs/` directory or contact the development team.