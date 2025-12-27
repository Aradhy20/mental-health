"""
Vercel serverless entrypoint for FastAPI
Maps the /api routes to the backend application.
"""
import sys
import os

# Ensure backend directory is in path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
backend_path = os.path.join(root_dir, 'backend')

sys.path.insert(0, backend_path)

try:
    from backend.api.index import app
except ImportError:
    try:
        from main import app
    except ImportError:
        from fastapi import FastAPI
        app = FastAPI()
        
        @app.get("/api")
        async def root():
            return {"message": "API entrypoint active in root/api/index.py"}

__all__ = ["app"]
