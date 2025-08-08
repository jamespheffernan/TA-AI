# Professor & Admin Guide

## Overview
This guide helps professors and administrators manage and maintain the TA AI Q&A Assistant.

### Professor Dashboard
- URL: `https://<your-app>.azurestaticapps.net/review`
- View recent student questions and AI responses.
- Flag incorrect answers and submit corrected responses.

### Course Management
1. Navigate to **Admin Panel**: `https://<your-app>.azurestaticapps.net/admin`
2. **Add Course**: Provide course name and description.
3. **Upload Materials**: Access the **Upload** page to upload PDF/PPTX files.

### User Access Controls
- Manage user roles (student, professor, admin).
- Use **Access Controls** in the Admin Panel to assign or revoke roles.

### Monitoring & Alerts
- Logging: Backend emits JSON logs with request timing by default.
- Tracing (optional): Set `ENABLE_OTEL=1` to enable OpenTelemetry spans.
- Azure Monitor: Configure OTLP endpoint and dashboards/grafana for visualization.
- Key metrics to watch:
  - Error rates >1%
  - Slow response times >1.5s (p95)
  - Function cold starts / throttling

### Deployment & Updates
1. Review CI pipeline status in GitHub Actions.
2. Update Terraform variables in `infrastructure/environments/prod/variables.tf`.
3. Run `terraform apply` to deploy updates.

### Support & Troubleshooting
- Refer to the **Operations Runbook** for rollback procedures.
- Contact DevOps team with resource IDs from the Admin Panel.

**End of Admin Guide**