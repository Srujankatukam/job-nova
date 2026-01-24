"""Avatar API routes"""
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from typing import Dict, Any
import logging
import uuid

from app.schemas.avatar import AvatarGenerateRequest, AvatarSession, AvatarStatusResponse
from app.services.tavus_service import tavus_service
from app.services.livekit_service import livekit_service
from app.websocket import websocket_endpoint, update_session_status

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/avatar/generate", response_model=AvatarSession)
async def generate_avatar(request: AvatarGenerateRequest):
    """Generate avatar video from text"""
    try:
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        # Initialize session status
        await update_session_status(session_id, "pending")
        
        # Start avatar generation asynchronously
        # In production, this would be handled by a background task
        import asyncio
        asyncio.create_task(_process_avatar_generation(session_id, request.text))
        
        return AvatarSession(
            sessionId=session_id,
            status="pending",
        )
    except Exception as e:
        logger.error(f"Error generating avatar: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate avatar: {str(e)}")


@router.get("/avatar/status/{session_id}", response_model=AvatarStatusResponse)
async def get_avatar_status(session_id: str):
    """Get avatar generation status"""
    try:
        # Check Tavus status (in a real implementation, this would check actual status)
        # For now, return a mock status
        return AvatarStatusResponse(
            sessionId=session_id,
            status="ready",  # Would check actual status
            progress=100,
            videoUrl="https://example.com/video.mp4",  # Would get from Tavus
        )
    except Exception as e:
        logger.error(f"Error getting avatar status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get avatar status")


@router.websocket("/ws/avatar/{session_id}")
async def websocket_route(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time avatar updates"""
    await websocket_endpoint(websocket, session_id)


@router.post("/avatar/livekit/token")
async def get_livekit_token(
    room_name: str,
    participant_name: str = "user"
):
    """Get LiveKit access token"""
    try:
        token = livekit_service.generate_token(
            room_name=room_name,
            participant_name=participant_name,
            can_publish=True,
            can_subscribe=True,
        )
        
        return {
            "token": token,
            "url": livekit_service.url or "wss://your-livekit-server.com",
            "room_name": room_name,
        }
    except Exception as e:
        logger.error(f"Error generating LiveKit token: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate LiveKit token")


async def _process_avatar_generation(session_id: str, text: str):
    """Background task to process avatar generation"""
    try:
        # Update status to generating
        await update_session_status(session_id, "generating", {"progress": 0})
        
        # Call Tavus API
        tavus_result = await tavus_service.generate_avatar(text)
        
        # Update status with Tavus replica ID
        await update_session_status(
            session_id,
            "generating",
            {
                "progress": 50,
                "tavus_replica_id": tavus_result.get("tavus_replica_id"),
            }
        )
        
        # Poll for completion (in production, use webhooks)
        # For now, simulate completion
        import asyncio
        await asyncio.sleep(2)  # Simulate processing time
        
        # Create LiveKit room
        room_info = livekit_service.create_room(f"avatar_{session_id}")
        
        # Update status to ready
        await update_session_status(
            session_id,
            "ready",
            {
                "progress": 100,
                "video_url": tavus_result.get("video_url"),
                "room_name": room_info.get("room_name"),
                "livekit_url": room_info.get("url"),
            }
        )
        
    except Exception as e:
        logger.error(f"Error processing avatar generation: {e}")
        await update_session_status(
            session_id,
            "error",
            {"error": str(e)}
        )

