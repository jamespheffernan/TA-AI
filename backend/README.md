# TA AI Backend (Azure Functions + FastAPI)

## Running Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the Azure Functions host:
   ```bash
   func start
   ```
   (Requires [Azure Functions Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local))

## Endpoints

- `GET /api/health` — Health check (returns `{ "status": "ok" }`)

## Project Structure

- `src/functions/` — Azure Functions HTTP triggers
- `src/services/` — Business logic and service classes
- `src/models/` — Pydantic models and schemas
- `src/utils/` — Utility functions

## Environment Variables

Copy `local.settings.json.example` to `local.settings.json` and fill in your secrets for local development.