"""
Main FastAPI application for TA AI backend
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import time
import uuid
import json
import logging
from datetime import datetime, timezone
from dotenv import load_dotenv
# Support running both as package (uvicorn src.main:app) and as script (python src/main.py)
try:
    from db import engine, Base  # when src/ is on sys.path
except ImportError:  # pragma: no cover
    from src.db import engine, Base  # fallback when launched as a package

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="TA AI API",
    description="AI-powered teaching assistant for university courses",
    version="0.1.0"
)

# Configure CORS
origins = [
    "http://localhost:3000",  # Next.js frontend
    "http://localhost:3001",  # Alternative port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "time": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        for key in (
            "request_id",
            "request_path",
            "request_method",
            "status_code",
            "duration_ms",
            "client_host",
            "user_agent",
        ):
            val = getattr(record, key, None)
            if val is not None:
                payload[key] = val
        return json.dumps(payload, ensure_ascii=False)


def setup_json_logging() -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(logging.INFO)


def setup_opentelemetry_if_enabled() -> None:
    if os.getenv("ENABLE_OTEL") != "1":
        return
    try:
        # Lazy import; optional dependency
        from opentelemetry import trace
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
        try:
            from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
            otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
            exporter = OTLPSpanExporter(endpoint=otlp_endpoint) if otlp_endpoint else ConsoleSpanExporter()
        except Exception:
            exporter = ConsoleSpanExporter()

        resource = Resource.create({"service.name": os.getenv("OTEL_SERVICE_NAME", "ta-ai-backend")})
        provider = TracerProvider(resource=resource)
        provider.add_span_processor(BatchSpanProcessor(exporter))
        trace.set_tracer_provider(provider)
        logging.getLogger("otel").info("OpenTelemetry tracing enabled")
    except Exception as e:
        logging.getLogger("otel").warning(f"OpenTelemetry not enabled: {e}")

@app.on_event("startup")
async def on_startup():
    # Import models to register metadata
    import src.models.models  # noqa: F401
    # Create database tables
    print("[Startup] Creating database tables...")
    Base.metadata.create_all(bind=engine)
    setup_json_logging()
    setup_opentelemetry_if_enabled()


@app.middleware("http")
async def access_log_middleware(request: Request, call_next):
    start = time.perf_counter()
    request_id = str(uuid.uuid4())
    status = 500
    span_ctx = None
    tracer = None
    try:
        # Optional span
        try:
            from opentelemetry import trace
            tracer = trace.get_tracer(__name__)
            span_ctx = tracer.start_as_current_span("http.request")
            span_ctx.__enter__()
        except Exception:
            tracer = None
    try:
        response = await call_next(request)
        status = response.status_code
        return response
    finally:
        if span_ctx is not None:
            try:
                span = trace.get_current_span()  # type: ignore[name-defined]
                if span is not None:
                    span.set_attribute("http.method", request.method)
                    span.set_attribute("http.target", request.url.path)
                    span.set_attribute("http.status_code", status)
            except Exception:
                pass
            try:
                span_ctx.__exit__(None, None, None)
            except Exception:
                pass
        duration_ms = int((time.perf_counter() - start) * 1000)
        logging.getLogger("access").info(
            "request",
            extra={
                "request_id": request_id,
                "request_path": request.url.path,
                "request_method": request.method,
                "status_code": locals().get("status", 500),
                "duration_ms": duration_ms,
                "client_host": request.client.host if request.client else None,
                "user_agent": request.headers.get("user-agent"),
            },
        )

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "TA AI API is running"}

@app.get("/api/test")
async def test_endpoint():
    """Test endpoint to verify API is accessible"""
    return {
        "message": "API is working",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

# QA query endpoint
from pydantic import BaseModel
try:
    from services.qa_service import generate_answer
except ImportError:  # pragma: no cover
    from src.services.qa_service import generate_answer

class QueryRequest(BaseModel):
    course_id: int
    question: str

@app.post("/api/query")
async def query_endpoint(req: QueryRequest):
    """Answer student question using QA service"""
    result = generate_answer(question=req.question, course_id=req.course_id)
    return result

# This allows running with uvicorn directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7071)