"""
FastAPI Entrypoint for Deployment Platforms
This file serves as the main entrypoint for deploying the Text Analysis Service
to platforms like Render, Railway, or Vercel.
"""
import sys
import os

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import the FastAPI app from text_service
try:
    from text_service.main import app
except ImportError as e:
    # Fallback: Create a minimal app if imports fail
    from fastapi import FastAPI
    
    app = FastAPI(title="Mental Health AI Service", version="1.0.0")
    
    @app.get("/")
    async def root():
        return {
            "message": "Mental Health AI Service",
            "status": "running",
            "note": "This is a fallback app. Configure environment properly for full functionality."
        }
    
    @app.get("/health")
    async def health():
        return {"status": "healthy", "service": "ai_service"}

# Export app for deployment platforms
__all__ = ["app"]
