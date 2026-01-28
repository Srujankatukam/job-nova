"""Pydantic schemas for Avatar API requests and responses"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class TavusStartRequest(BaseModel):
    """Request to start a new Tavus conversation"""
    conversation_name: Optional[str] = Field(None, description="Optional name for the conversation")
    custom_greeting: Optional[str] = Field(
        None,
        description="Custom greeting or context for the avatar"
    )


class LiveKitTokenRequest(BaseModel):
    """Request to generate LiveKit access token"""
    room_name: str = Field(..., description="Name of the LiveKit room")
    participant_name: str = Field(..., description="Display name of the participant")
    participant_identity: Optional[str] = Field(None, description="Unique identity for the participant")


class TavusSendRequest(BaseModel):
    """Request to send a message to Tavus avatar"""
    conversation_id: str = Field(..., description="Tavus conversation ID")
    text: str = Field(..., min_length=1, max_length=5000, description="Message text to send")


class TavusStartResponse(BaseModel):
    """Response after starting a Tavus conversation"""
    conversation_id: str = Field(..., description="Unique conversation ID")
    livekit_room_name: str = Field(..., description="LiveKit room name for streaming")
    livekit_token: str = Field(..., description="LiveKit access token for user")
    livekit_url: str = Field(..., description="LiveKit server URL")
    tavus_data: Dict[str, Any] = Field(..., description="Raw Tavus API response")
    status: str = Field(default="active", description="Conversation status")


class TavusStatusResponse(BaseModel):
    """Response for conversation status"""
    conversation_id: str = Field(..., description="Conversation ID")
    status: str = Field(..., description="Conversation status")
    created_at: Optional[str] = Field(None, description="Creation timestamp")
    ended_at: Optional[str] = Field(None, description="End timestamp")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class TavusEndResponse(BaseModel):
    """Response after ending a conversation"""
    conversation_id: str = Field(..., description="Conversation ID")
    success: bool = Field(..., description="Whether the conversation was ended successfully")
    message: str = Field(default="Conversation ended", description="Status message")


class LiveKitTokenResponse(BaseModel):
    """Response with LiveKit access token"""
    token: str = Field(..., description="JWT access token")
    url: str = Field(..., description="LiveKit server URL")
    room_name: str = Field(..., description="Room name")


class ErrorResponse(BaseModel):
    """Error response"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
