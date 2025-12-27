import sys
import os

# Add root and backend directories to sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_dir = os.path.join(root_dir, 'backend')

if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

try:
    # Try importing as a package from root
    from backend.api.index import app
except ImportError:
    try:
        # Try importing directly if backend_dir is in path
        from api.index import app as backend_app
        app = backend_app
    except ImportError:
        from fastapi import FastAPI
        app = FastAPI()
        @app.get("/api/health")
        async def health():
            return {"status": "error", "message": "Could not import backend app"}

__all__ = ["app"]

