"""API router for Avatar (Tavus + LiveKit) endpoints"""
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
import logging
from datetime import datetime

from app.schemas.avatar_schemas import (
    TavusStartRequest,
    TavusStartResponse,
    TavusSendRequest,
    TavusStatusResponse,
    TavusEndResponse,
    TavusEndResponse,
    LiveKitTokenRequest,
    LiveKitTokenResponse,
    ErrorResponse,
)
from app.services.tavus_service import get_tavus_service
from app.services.livekit_service import get_livekit_service
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/avatar", tags=["avatar"])


@router.post("/tavus/start", response_model=TavusStartResponse)
async def start_tavus_conversation(request: TavusStartRequest):
    """
    Start a new Tavus Persona conversation with LiveKit streaming
    
    This endpoint:
    1. Creates a Tavus conversation with the configured persona
    2. Creates a LiveKit room for real-time streaming
    3. Generates a LiveKit access token for the user
    4. Returns all connection details
    """
    try:
        tavus_service = get_tavus_service()
        
        # Create Tavus conversation
        logger.info("Creating Tavus conversation...")
        tavus_data = await tavus_service.create_conversation(
            conversation_name=request.conversation_name,
            custom_greeting=request.custom_greeting,
        )
        
        conversation_id = tavus_data.get("conversation_id")
        if not conversation_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get conversation ID from Tavus"
            )
        
        # Tavus Persona API provides a conversation_url that contains all connection details
        # The frontend should use this URL directly to connect via WebRTC
        conversation_url = tavus_data.get("conversation_url", "")
        
        logger.info(f"Successfully started conversation: {conversation_id}")
        logger.info(f"Conversation URL: {conversation_url}")
        
        # Return the Tavus data directly - Tavus handles LiveKit internally
        return TavusStartResponse(
            conversation_id=conversation_id,
            livekit_room_name=f"tavus_{conversation_id}",  # Not actually used
            livekit_token=conversation_url,  # Pass the conversation URL  
            livekit_url=conversation_url,  # Use conversation URL
            tavus_data=tavus_data,
            status="active",
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting Tavus conversation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start conversation: {str(e)}"
        )


@router.post("/tavus/send", status_code=status.HTTP_200_OK)
async def send_message_to_tavus(request: TavusSendRequest):
    """
    Send a text message to the Tavus avatar
    
    Note: Messages are typically sent via LiveKit data channel in real-time.
    This endpoint logs the message for tracking purposes.
    """
    try:
        tavus_service = get_tavus_service()
        
        logger.info(f"Sending message to conversation {request.conversation_id}")
        success = await tavus_service.send_message(
            conversation_id=request.conversation_id,
            text=request.text,
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send message"
            )
        
        return {"success": True, "message": "Message sent successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending message: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send message: {str(e)}"
        )


@router.delete("/tavus/end/{conversation_id}", response_model=TavusEndResponse)
async def end_tavus_conversation(conversation_id: str):
    """
    End a Tavus conversation and cleanup resources
    
    This endpoint:
    1. Ends the Tavus conversation
    2. Deletes the associated LiveKit room
    3. Cleans up any stored metadata
    """
    try:
        tavus_service = get_tavus_service()
        livekit_service = get_livekit_service()
        
        logger.info(f"Ending conversation: {conversation_id}")
        
        # End Tavus conversation
        success = await tavus_service.end_conversation(conversation_id)
        
        # Delete LiveKit room
        room_name = f"tavus_{conversation_id}"
        try:
            await livekit_service.delete_room(room_name)
        except Exception as e:
            logger.warning(f"Could not delete LiveKit room: {str(e)}")
        
        return TavusEndResponse(
            conversation_id=conversation_id,
            success=success,
            message="Conversation ended successfully" if success else "Failed to end conversation",
        )
        
    except Exception as e:
        logger.error(f"Error ending conversation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to end conversation: {str(e)}"
        )


@router.get("/tavus/status/{conversation_id}", response_model=TavusStatusResponse)
async def get_conversation_status(conversation_id: str):
    """
    Get the status of a Tavus conversation
    """
    try:
        tavus_service = get_tavus_service()
        
        status_data = await tavus_service.get_conversation_status(conversation_id)
        
        return TavusStatusResponse(
            conversation_id=conversation_id,
            status=status_data.get("status", "unknown"),
            created_at=status_data.get("created_at"),
            ended_at=status_data.get("ended_at"),
            metadata=status_data.get("metadata"),
        )
        
    except Exception as e:
        logger.error(f"Error getting conversation status: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get conversation status: {str(e)}"
        )


@router.post("/livekit/token", response_model=LiveKitTokenResponse)
async def generate_livekit_token(request: LiveKitTokenRequest):
    """
    Generate a LiveKit access token for a participant
    
    This is used for:
    - Joining existing rooms
    - Refreshing expired tokens
    - Adding additional participants
    """
    try:
        livekit_service = get_livekit_service()
        
        participant_identity = request.participant_identity or f"user_{datetime.now().timestamp()}"
        
        logger.info(f"Generating LiveKit token for {participant_identity}")
        token = livekit_service.generate_token(
            room_name=request.room_name,
            participant_identity=participant_identity,
            participant_name=request.participant_name,
            can_publish=True,
            can_subscribe=True,
            can_publish_data=True,
            token_ttl=3600,
        )
        
        return LiveKitTokenResponse(
            token=token,
            url=settings.LIVEKIT_URL or "ws://localhost:7880",
            room_name=request.room_name,
        )
        
    except Exception as e:
        logger.error(f"Error generating LiveKit token: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate token: {str(e)}"
        )
