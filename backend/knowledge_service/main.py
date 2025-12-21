import sys
import os

# Add the shared directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

from fastapi import FastAPI, HTTPException, Body, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import uuid

# Import vector database
from ..text_service.vector_db import vector_db

app = FastAPI(title="Knowledge Management Service", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create API Router
router = APIRouter()

class KnowledgeDocument(BaseModel):
    id: Optional[str] = None
    content: str
    category: str
    severity: str

class KnowledgeQuery(BaseModel):
    query: str
    n_results: Optional[int] = 3

class QueryResponse(BaseModel):
    results: List[Dict]
    message: str

class AddDocumentResponse(BaseModel):
    document_id: str
    message: str

class HealthResponse(BaseModel):
    status: str
    message: str

@router.post("/knowledge/add", response_model=AddDocumentResponse)
async def add_knowledge_document(document: KnowledgeDocument):
    """
    Add a new document to the mental health knowledge base
    """
    try:
        # Generate ID if not provided
        doc_id = document.id or f"mhk_{uuid.uuid4().hex[:8]}"
        
        # Prepare document for vector database
        doc_data = {
            "id": doc_id,
            "content": document.content,
            "category": document.category,
            "severity": document.severity
        }
        
        # Add to vector database
        vector_db.add_documents([doc_data])
        
        return AddDocumentResponse(
            document_id=doc_id,
            message="Document added successfully to knowledge base"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add document: {str(e)}")

@router.post("/knowledge/query", response_model=QueryResponse)
async def query_knowledge_base(query_data: KnowledgeQuery):
    """
    Query the mental health knowledge base using semantic search
    """
    try:
        # Search for similar documents
        results = vector_db.search_similar_documents(query_data.query, query_data.n_results)
        
        return QueryResponse(
            results=results,
            message=f"Found {len(results)} relevant documents"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to query knowledge base: {str(e)}")

@router.get("/knowledge/document/{doc_id}")
async def get_knowledge_document(doc_id: str):
    """
    Retrieve a specific document by ID from the knowledge base
    """
    try:
        document = vector_db.get_document_by_id(doc_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return {
            "document": document,
            "message": "Document retrieved successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve document: {str(e)}")

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    """
    return HealthResponse(
        status="healthy",
        message="Knowledge Management Service is running"
    )

@app.get("/", response_model=HealthResponse)
async def root():
    """
    Root endpoint
    """
    return HealthResponse(
        status="healthy",
        message="Knowledge Management Service is running"
    )

# Include the router with prefix
app.include_router(router, prefix="/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8009)