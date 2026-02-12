from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from db import get_db
from models import ChatMessage, User
from utils.ai_response import get_completion
from schemas.ai_response_schemas import AIRequest, AIResponse, ChatHistoryResponse, SessionListResponse, SessionSchema
from utils.jwt_handler import verify_token
from typing import Optional
from sqlalchemy import func
import uuid

router = APIRouter()

def get_current_user_id(authorization: Optional[str] = Header(None)) -> Optional[int]:
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        payload = verify_token(token)
        if payload:
            return int(payload.get("sub"))
    return None

@router.post("/ask", response_model=AIResponse)
def ask_ai(request: AIRequest, db: Session = Depends(get_db), user_id: Optional[int] = Depends(get_current_user_id)):
    """Get response from AI model and optionally save to history."""
    print(f"DEBUG: ask_ai called. user_id={user_id}, session_id={request.session_id}")
    try:
        response_content = get_completion(request.message, request.system_prompt)
        
        session_id = request.session_id or str(uuid.uuid4())
        print(f"DEBUG: Using session_id={session_id}")
        
        if user_id:
            # Check if session exists to get title, or use first 30 chars of message
            title = request.message[:30] + ("..." if len(request.message) > 30 else "")
            
            # Save user message
            user_msg = ChatMessage(user_id=user_id, session_id=session_id, session_title=title, role="user", content=request.message)
            # Save assistant response
            ai_msg = ChatMessage(user_id=user_id, session_id=session_id, session_title=title, role="assistant", content=response_content)
            db.add(user_msg)
            db.add(ai_msg)
            db.commit()
            print("DEBUG: Messages saved to DB")
        else:
            print("DEBUG: No user_id, skipping DB save")

        return AIResponse(response=response_content, session_id=session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions", response_model=SessionListResponse)
def get_sessions(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    """Get list of unique chat sessions for the authenticated user."""
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    import traceback
    try:
        sessions_query = db.query(
            ChatMessage.session_id,
            func.min(ChatMessage.session_title),
            func.max(ChatMessage.timestamp).label("last_message_at")
        ).filter(ChatMessage.user_id == user_id, ChatMessage.session_id != None).group_by(ChatMessage.session_id).order_by(func.max(ChatMessage.timestamp).desc()).all()
        
        print(f"DEBUG: get_sessions query result: {sessions_query}")
        
        sessions = [SessionSchema(session_id=s[0], title=s[1] or "New Chat", last_message_at=s[2]) for s in sessions_query]
        print(f"DEBUG: Sessions mapped: {sessions}")
        return SessionListResponse(sessions=sessions)
    except Exception as e:
        with open("error.log", "w") as f:
            f.write(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{session_id}", response_model=ChatHistoryResponse)
def get_session_history(session_id: str, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    """Get chat history for a specific session."""
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    messages = db.query(ChatMessage).filter(ChatMessage.user_id == user_id, ChatMessage.session_id == session_id).order_by(ChatMessage.timestamp.asc()).all()
    return ChatHistoryResponse(history=messages)

@router.get("/history", response_model=ChatHistoryResponse)
def get_all_history(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    """Get all chat history for the authenticated user."""
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    messages = db.query(ChatMessage).filter(ChatMessage.user_id == user_id).order_by(ChatMessage.timestamp.asc()).all()
    return ChatHistoryResponse(history=messages)
    