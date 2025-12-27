"""
Root Entrypoint for FastAPI
This file satisfies Vercel's requirement for a FastAPI entrypoint if the root directory is used.
It proxies requests to the main backend application in the /backend directory.
"""
import sys
import os

# Add the backend directory to the path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
if os.path.exists(backend_path):
    sys.path.insert(0, backend_path)
    try:
        from backend.main import app
    except ImportError:
        # Fallback if the path structure is different
        try:
            from main import app
        except ImportError:
            # Create a basic app if everything else fails to prevent deployment error
            from fastapi import FastAPI
            app = FastAPI()
            
            @app.get("/")
            async def info():
                return {"message": "Root API entrypoint active. Backend imports failed."}
else:
    # Basic fallback app
    from fastapi import FastAPI
    app = FastAPI()
    
    @app.get("/")
    async def status():
        return {"message": "Backend directory not found in root."}

# Export the app variable for Vercel
__all__ = ["app"]
