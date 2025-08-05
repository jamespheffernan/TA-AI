Below is a check-list you (or your cloud/IT lead) must complete outside the code-base to stand-up the MVP stack described earlier.  Follow it in order; each line is actionable, and nothing requires you to open the IDE.

⸻

0. Prerequisites (30 min)
	1.	Azure subscription with pay-as-you-go or credits – if you don’t have one, create at https://azure.microsoft.com.
	2.	Owner or Contributor role on that subscription (needed to create resources).
	3.	A Microsoft Entra ID tenant (formerly AAD). Your Azure subscription is automatically linked to one; you’ll use it for SSO.

⸻

1. Request Azure OpenAI access (10 min form + 1-3 days approval)

You cannot skip this – the OpenAI resource is gated per tenant.

	•	Go to Azure OpenAI Service > Apply: https://aka.ms/oai/apply.
	•	Use your academic email; choose Education use-case, mention “course Q&A assistant”.
	•	Wait for the “approved” email (typically < 72 h for universities).

⸻

2. Create the core resource group & VNet (5 min)

RG = ta-mvp-rg            # all resources live here
Location = UK South
VNet 10.20.0.0/16
    ├─ subnet functions   10.20.1.0/24
    └─ subnet db          10.20.2.0/24

Portal route ► Create resource ⟶ Virtual Network; name it ta-mvp-vnet.  Add two sub-nets as above.

⸻

3. Spin up Azure OpenAI in the VNet (~10 min)
	1.	Create ► Azure OpenAI
	•	Resource group: ta-mvp-rg
	•	Name: ta-mvp-openai
	•	Region: UK South (has GPT-4 Turbo & embeddings)
	2.	Deploy models
	•	In the resource blade → Deployments → + Create ▸ choose:
	•	gpt-4-turbo  (deployment name: gpt4turbo)
	•	text-embedding-3-small (deployment name: embed-small)
	3.	Lock it to private network
	•	Networking ▸ Allow access from: Disabled
	•	Add Private Endpoint to ta-mvp-vnet / subnet functions, accepting defaults  .
	•	Azure auto-creates a private DNS zone. Confirm *.openai.azure.com is linked to the VNet.
	4.	Grab credentials
	•	Keys & Endpoint tab → copy Key 1 and the endpoint URL (save to password manager – you’ll drop them into environment variables later).

⸻

4. Provision Postgres + pgvector (~10 min)
	1.	Create ► Azure Database for PostgreSQL Flexible Server
	•	Name: ta-mvp-db
	•	Pricing tier: Basic, 1 vCore, 64 GiB storage (≈ £20 / mo).
	•	Networking: Private access → VNet ta-mvp-vnet ▸ subnet db.
	2.	Once the server is up, enable pgvector:
	•	Server Parameters ▸ add vector to azure.extensions and save  .
	•	Connect via psql and run:

CREATE EXTENSION IF NOT EXISTS vector;
CREATE DATABASE ta_mvp;


	3.	Copy the (private) host name, admin user, and generated password.

⸻

5. Register Entra ID applications for SSO (~10 min)

App	Type	Redirect / Scope	Secrets
ai-ta-frontend	SPA / Public client	https://<staticapp>.azurestaticapps.net/.auth/login/aad/callback	—
ai-ta-backend	Web API	Expose scope api://<app-id>/Chat.Access	create 1 client secret

Steps:
	1.	Entra ID ▸ App registrations ▸ New registration (twice).
	2.	For ai-ta-frontend, enable Access tokens (SPA) under Authentication.
	3.	For ai-ta-backend, add Redirect URI https://localhost/auth-oidc/callback (for local testing) and the production Function URL once deployed.
	4.	Note Tenant ID, Client IDs, and the backend Client Secret.

⸻

6. Create Function App + VNet integration (~10 min)
	1.	Create ► Function App
	•	Name: ta-mvp-fn
	•	Runtime: Python 3.11, Consumption plan.
	•	Region: UK South, same RG.
	2.	Networking ▸ VNet integration ▸ select subnet functions.
	3.	Configuration ▸ Application settings – add:

OPENAI_API_KEY   = <Key 1>
OPENAI_ENDPOINT  = https://ta-mvp-openai.openai.azure.com/
OPENAI_GPT_DEPLOYMENT = gpt4turbo
OPENAI_EMBED_DEPLOYMENT = embed-small
PG_HOST          = ta-mvp-db.private.postgres.database.azure.com
PG_DB            = ta_mvp
PG_USER          = <admin_user>
PG_PASSWORD      = <pw>
AAD_TENANT_ID    = <tenant_id>
AAD_CLIENT_ID    = <backend app client id>
AAD_CLIENT_SECRET= <backend secret>

	4.	Identity ▸ enable System-assigned managed identity (optional) so you can later swap from key-based to RBAC access.

⸻

7. Spin up Static Web App (~5 min)
	1.	Create ► Static Web Apps
	•	Name: ta-mvp-ui
	•	Deploy from GitHub repo (or manual upload).
	•	Once built, note the default URL https://<hash>.azurestaticapps.net.
	2.	In the SWA portal ▸ Authentication → choose Azure Active Directory, point it to ai-ta-frontend app ID.
	3.	Add the SWA URL to the frontend app’s SPA redirect list (step 5 above).

⸻

8. Set cost guard-rails (5 min)
	•	Cost Management ▸ Budgets – create a monthly budget of £80 with email alert.
	•	Advisor ▸ Recommendations – enable cost optimisation alerts.

⸻

9. Smoke-test connectivity (~10 min)
	1.	In App Service Logs enable application logging (filesystem) for Functions.
	2.	Hit /healthz route – should return OK.
	3.	Manually run an ingestion HTTP trigger with a tiny markdown file; verify rows appear in chunks table.
	4.	Ask a sample question via /chat route; ensure GPT-4 Turbo responds and citations point to the chunk IDs.

⸻

10. Upload course materials
	•	Use the upload portal (or az storage blob upload) to push PDFs/PPTX.
	•	Confirm embeddings are created and the vector count in Postgres matches chunk count.

⸻

11. Invite pilot users
	1.	Professor logs in via SWA AAD and verifies dashboard shows logs.
	2.	Provide students the SWA URL; they’ll use their institutional OIDC credentials automatically.

⸻

You’re live 🎉

Latency should be < 1.5 s per query; total burn ≈ £50 / mo (monitor in Cost Management).  When usage climbs, revisit the Upgrade Path table from the MVP doc.

⸻

Key docs if you get stuck
	•	Private Endpoints for Azure OpenAI – step-by-step screenshots  
	•	Enable pgvector on Azure Postgres Flexible Server – extension guide  
	•	Model deployment list & regions – check availability of GPT-4 Turbo / embedding-3-small   