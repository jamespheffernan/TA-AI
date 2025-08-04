"""
Main FastAPI application for TA AI backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from .db import engine, Base

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

@app.on_event("startup")
async def on_startup():
    # Import models to register metadata
    import src.models.models  # noqa: F401
    # Create database tables
    print("[Startup] Creating database tables...")
    Base.metadata.create_all(bind=engine)

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

# This allows running with uvicorn directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7071)