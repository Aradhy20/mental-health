"""
Enhanced AI Assistant Service
FastAPI service for personalized mental health support
"""

from fastapi import FastAPI, HTTPException, APIRouter, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from dotenv import load_dotenv
import sys
import os

# Add paths
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..'))

# Import shared utilities
from shared.cache import cache_model
from shared.logging_config import setup_logger
from shared.monitoring import track_performance, RequestTimer, monitor
from shared.middleware import RequestIDMiddleware, PerformanceMiddleware, ErrorLoggingMiddleware

# Import assistant components
from ai_models.assistant.assistant_engine import AssistantEngine, LLMProvider
from ai_models.assistant.personality import PersonalityType

# Load environment variables
load_dotenv()

# Setup logger
logger = setup_logger(
    "assistant_service",
    log_level="INFO",
    log_dir="backend/logs",
    use_json=False
)

logger.info("Initializing AI Assistant Service...")

# Initialize FastAPI app
app = FastAPI(
    title="AI Assistant Service",
    version="1.0.0",
    description="Personalized mental health AI assistant"
)

# Add middleware
app.add_middleware(ErrorLoggingMiddleware, logger=logger)
app.add_middleware(PerformanceMiddleware, logger=logger)
app.add_middleware(RequestIDMiddleware)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class ChatRequest(BaseModel):
    user_id: int
    message: str
    emotion_data: Optional[dict] = None
    personality: Optional[str] = "empathetic"

class ChatResponse(BaseModel):
    response: str
    crisis_detected: bool
    metadata: dict

class ConversationHistoryResponse(BaseModel):
    messages: List[dict]
    summary: dict

# Create API Router
router = APIRouter()

# Cached assistant initialization
@cache_model("assistant_engine")
def get_assistant():
    """Get or create the assistant engine (cached)"""
    logger.info("Initializing AI Assistant Engine...")
    return AssistantEngine(
        provider=LLMProvider.MOCK,  # Change to OPENAI or OLLAMA in production
        personality_type=PersonalityType.EMPATHETIC
    )

# Routes
@router.post("/chat", response_model=ChatResponse)
@track_performance("chat")
async def chat(request_data: ChatRequest, request: Request):
    """
    Chat with AI assistant
    """
    request_id = getattr(request.state, "request_id", "unknown")
    logger.info(
        f"Chat request from user {request_data.user_id}",
        extra={"request_id": request_id}
    )
    
    try:
        # Get assistant
        with RequestTimer("get_assistant", logger):
            assistant = get_assistant()
        
        # Change personality if requested
        if request_data.personality:
            try:
                p_type = PersonalityType(request_data.personality.lower())
                assistant.change_personality(p_type)
            except ValueError:
                logger.warning(f"Invalid personality: {request_data.personality}")
        
        # Generate response
        with RequestTimer("generate_response", logger):
            result = assistant.generate_response(
                user_id=request_data.user_id,
                user_message=request_data.message,
                emotion_data=request_data.emotion_data
            )
        
        logger.info(
            f"Chat response generated (crisis: {result['crisis_detected']})",
            extra={"request_id": request_id}
        )
        monitor.increment_requests("chat")
        
        return ChatResponse(
            response=result["response"],
            crisis_detected=result["crisis_detected"],
            metadata=result["metadata"]
        )
    
    except Exception as e:
        logger.error(f"Chat failed: {str(e)}", extra={"request_id": request_id}, exc_info=True)
        monitor.increment_errors("chat")
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

@router.get("/conversation/{user_id}", response_model=ConversationHistoryResponse)
@track_performance("get_conversation")
async def get_conversation(user_id: int):
    """Get conversation history for a user"""
    try:
        assistant = get_assistant()
        
        history = assistant.conversation_manager.get_conversation_history(user_id)
        summary = assistant.conversation_manager.get_conversation_summary(user_id)
        
        monitor.increment_requests("get_conversation")
        
        return ConversationHistoryResponse(
            messages=history,
            summary=summary
        )
    
    except Exception as e:
        logger.error(f"Failed to get conversation: {str(e)}", exc_info=True)
        monitor.increment_errors("get_conversation")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/conversation/{user_id}")
@track_performance("clear_conversation")
async def clear_conversation(user_id: int):
    """Clear conversation history"""
    try:
        assistant = get_assistant()
        assistant.clear_conversation(user_id)
        
        monitor.increment_requests("clear_conversation")
        return {"message": "Conversation cleared successfully"}
    
    except Exception as e:
        logger.error(f"Failed to clear conversation: {str(e)}", exc_info=True)
        monitor.increment_errors("clear_conversation")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/personalities")
async def get_personalities():
    """Get available personality types"""
    return {
        "personalities": [
            {
                "type": p.value,
                "description": f"{p.value.capitalize()} personality"
            }
            for p in PersonalityType
        ]
    }

@app.get("/")
async def root():
    return {
        "message": "AI Assistant Service v1.0",
        "features": [
            "emotion-aware_responses",
            "crisis_detection",
            "multiple_personalities",
            "conversation_history"
        ]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "assistant_service",
        "version": "1.0.0"
    }

@app.get("/metrics")
async def get_metrics():
    """Get performance metrics"""
    from shared.monitoring import get_performance_report
    return get_performance_report()

# Include router
app.include_router(router, prefix="/v1")

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Service starting up - warming cache...")
    get_assistant()
    logger.info("Assistant loaded - service ready")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8009)
