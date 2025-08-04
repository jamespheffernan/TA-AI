#!/usr/bin/env python
"""
Local development server for TA AI backend
Run this instead of Azure Functions for local development
"""
import uvicorn

if __name__ == "__main__":
    # Run the FastAPI app
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=7071,
        reload=True,
        log_level="info"
    )