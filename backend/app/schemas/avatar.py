"""Pydantic schemas for Avatar entities"""
from pydantic import BaseModel, Field
from typing import Optional


class AvatarGenerateRequest(BaseModel):
    """Request schema for avatar generation"""
    text: str = Field(..., min_length=1, max_length=5000)


class AvatarSession(BaseModel):
    """Schema for avatar session"""
    sessionId: str
    status: str = Field(..., pattern="^(pending|generating|ready|error)$")
    videoUrl: Optional[str] = None
    audioUrl: Optional[str] = None
    error: Optional[str] = None


class AvatarStatusResponse(BaseModel):
    """Response schema for avatar status"""
    sessionId: str
    status: str
    progress: Optional[float] = Field(None, ge=0, le=100)
    videoUrl: Optional[str] = None
    audioUrl: Optional[str] = None
    error: Optional[str] = None

