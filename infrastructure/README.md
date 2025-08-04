# Infrastructure as Code (IaC) for TA AI

This directory contains Terraform modules and environment configurations for deploying the TA AI MVP on Azure.

## Structure

```
modules/           # Reusable Terraform modules for each Azure resource
  resource_group/
  vnet/
  postgres/
  openai/
  storage/
  staticwebapp/
  functions/
environments/
  dev/             # Example environment (dev)
    main.tf
    variables.tf
    backend.tf
```

## Prerequisites
- [Terraform 1.4+](https://www.terraform.io/downloads.html)
- Azure CLI authenticated (`az login`)
- Sufficient permissions to create resources in your Azure subscription

## Quickstart

1. **Navigate to the environment directory:**
   ```bash
   cd infrastructure/environments/dev
   ```
2. **Initialize Terraform:**
   ```bash
   terraform init
   ```
3. **Review the plan:**
   ```bash
   terraform plan
   ```
4. **Apply the plan:**
   ```bash
   terraform apply
   ```

> **Note:** All resource names, credentials, and IDs are placeholders. Update `variables.tf` and module inputs as needed for your environment.

## Modules
- **resource_group**: Azure Resource Group
- **vnet**: Virtual Network with subnets for Postgres, OpenAI, Functions
- **postgres**: PostgreSQL Flexible Server (with pgvector)
- **openai**: Azure OpenAI resource with Private Endpoint
- **storage**: Azure Storage Account
- **staticwebapp**: Azure Static Web App (for Next.js frontend)
- **functions**: Azure Functions (Python backend)

## Security
- All sensitive values (passwords, keys) are placeholders. Use a secrets manager or environment variables for production.
- Private Endpoints and VNet integration are scaffolded but may require further configuration for production.

## Next Steps
- Parameterize modules for production use
- Add remote backend (e.g., Azure Storage) for state management
- Integrate with CI/CD pipeline