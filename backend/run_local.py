#!/usr/bin/env python
"""
Local development server for TA AI backend
Run this instead of Azure Functions for local development
"""
import os, sys
# Ensure backend/src is on Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import uvicorn

if __name__ == "__main__":
    # Run the FastAPI app
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=7071,
        reload=False,
        log_level="info"
    )