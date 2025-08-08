# Launch Checklist

This checklist ensures the TA AI Q&A Assistant meets all requirements before production launch.

## Functional Validation
- [ ] Ingestion: Able to upload and ingest PDF/PPTX documents end-to-end
- [ ] Embeddings: Verify vectors stored in Postgres pgvector
- [ ] QA Service: `/api/query` returns answers with correct citations under 1.5s
- [ ] Chat UI: Students can ask questions, view answers, and click citations
- [ ] Professor Dashboard: Flags and feedback persist correctly
- [ ] Course Management: Courses can be added/edited/deleted in Admin Panel
- [ ] User Access: SSO login works for student, professor, and admin roles

## Security Validation
- [ ] Private Endpoints: Database and OpenAI do not receive public traffic
- [ ] HTTPS Only: All endpoints enforce TLS
- [ ] API Auth: `x-api-key` header protects backend functions
- [ ] Input Sanitization: Validate and sanitize all user inputs
- [ ] Least Privilege: Azure roles scoped properly

## Performance & Monitoring
- [ ] Load Test: Health and QA endpoints handle 200 concurrent users under thresholds
- [ ] Monitoring: JSON logs ingested; OTEL traces exported to Azure Monitor/Grafana
- [ ] Alerts: Error rate and latency alerts configured in Azure Monitor

## Cost Review
- [ ] Cost Estimates: Monthly costs remain under $100 (OpenAI, Postgres, Functions)
- [ ] Autoscale Settings: Verify scaling rules for Functions

## Deployment & Operational
- [ ] CI/CD: GitHub Actions pipeline passes for lint, test, build, and Terraform plan
- [ ] Terraform Apply: Dev environment provisioned successfully
- [ ] Documentation: User and Admin guides available in `docs/`
- [ ] Runbook: Operations runbook updated with rollback steps

## Signoff
- [ ] Professor signoff on response quality
- [ ] Developer signoff on infrastructure readiness
- [ ] Ready for production deploy