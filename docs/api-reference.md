# API Reference

## Authentication
- Header: `x-api-key: <API_KEY_SECRET>`
- Content-Type: `application/json`

## Health
- Method: GET
- Path: `/api/health`
- Response: `200 OK`
```json
{ "status": "ok", "message": "TA AI API is running" }
```

## Query
- Method: POST
- Path: `/api/query`
- Headers: `x-api-key`
- Body:
```json
{ "course_id": 1, "question": "What is entropy?" }
```
- Response `200 OK`:
```json
{ "answer": "...", "citations": [1, 2, 3] }
```

## Ingest (Azure Function)
- Method: POST
- Path: `/api/ingest` (Functions app)
- Headers: `x-api-key`
- Body:
```json
{ "course_id": 1, "path": "/path/to/file.pdf" }
```
- Response `200 OK`:
```json
{ "course_id": 1, "chunks_created": 123 }
```

## Environment Variables
- `API_KEY_SECRET` (required)
- `OPENAI_API_KEY` or `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_VERSION` (if using Azure OpenAI)
- `EMBEDDING_MODEL` (default `text-embedding-3-small`)
- `KNN_K` (default 5)
- `DATABASE_URL` (default local SQLite)
- `ENABLE_OTEL` (set `1` to enable tracing)
- `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_SERVICE_NAME`

