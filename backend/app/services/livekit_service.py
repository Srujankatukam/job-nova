"""LiveKit service for real-time audio/video streaming"""
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import uuid

try:
    from livekit import api
    from livekit.protocol import models
    LIVEKIT_AVAILABLE = True
except ImportError:
    LIVEKIT_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("LiveKit SDK not available, using mock implementation")

from app.config import settings

logger = logging.getLogger(__name__)


class LiveKitService:
    """Service for LiveKit real-time streaming"""
    
    def __init__(self):
        self.url = settings.LIVEKIT_URL
        self.api_key = settings.LIVEKIT_API_KEY
        self.api_secret = settings.LIVEKIT_API_SECRET
        
        if LIVEKIT_AVAILABLE and self.api_key and self.api_secret:
            self.livekit_api = api.LiveKitAPI(
                url=self.url or "https://your-livekit-server.com",
                api_key=self.api_key,
                api_secret=self.api_secret,
            )
        else:
            self.livekit_api = None
            logger.warning("LiveKit not fully configured, using mock mode")
    
    def create_room(self, room_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a LiveKit room
        
        Args:
            room_name: Optional room name (generates UUID if not provided)
        
        Returns:
            Dictionary with room name and connection details
        """
        if not room_name:
            room_name = f"room_{uuid.uuid4().hex[:8]}"
        
        if self.livekit_api:
            try:
                # Create room using LiveKit API
                room = self.livekit_api.room.create_room(
                    models.CreateRoomRequest(
                        name=room_name,
                        empty_timeout=300,  # 5 minutes
                        max_participants=10,
                    )
                )
                
                return {
                    "room_name": room.name,
                    "room_sid": room.sid,
                    "url": self.url,
                }
            except Exception as e:
                logger.error(f"Error creating LiveKit room: {e}")
                return self._mock_create_room(room_name)
        else:
            return self._mock_create_room(room_name)
    
    def generate_token(
        self,
        room_name: str,
        participant_name: str,
        participant_identity: Optional[str] = None,
        can_publish: bool = True,
        can_subscribe: bool = True,
    ) -> str:
        """
        Generate access token for LiveKit room
        
        Args:
            room_name: Name of the room
            participant_name: Name of the participant
            participant_identity: Optional identity (uses name if not provided)
            can_publish: Whether participant can publish
            can_subscribe: Whether participant can subscribe
        
        Returns:
            JWT token string
        """
        if not participant_identity:
            participant_identity = participant_name
        
        if self.livekit_api and self.api_key and self.api_secret:
            try:
                # Generate token using LiveKit
                grant = models.VideoGrant(
                    room_join=True,
                    room=room_name,
                    can_publish=can_publish,
                    can_subscribe=can_subscribe,
                )
                
                token = api.AccessToken(self.api_key, self.api_secret) \
                    .with_identity(participant_identity) \
                    .with_name(participant_name) \
                    .with_grant(grant) \
                    .to_jwt()
                
                return token
            except Exception as e:
                logger.error(f"Error generating LiveKit token: {e}")
                return self._mock_token(room_name, participant_name)
        else:
            return self._mock_token(room_name, participant_name)
    
    def _mock_create_room(self, room_name: str) -> Dict[str, Any]:
        """Mock room creation for development"""
        logger.info(f"Mock LiveKit room creation: {room_name}")
        return {
            "room_name": room_name,
            "room_sid": f"mock_{uuid.uuid4().hex[:8]}",
            "url": self.url or "wss://mock-livekit-server.com",
        }
    
    def _mock_token(self, room_name: str, participant_name: str) -> str:
        """Mock token generation for development"""
        logger.info(f"Mock LiveKit token for {participant_name} in {room_name}")
        return f"mock_token_{room_name}_{participant_name}_{uuid.uuid4().hex[:8]}"


# Global instance
livekit_service = LiveKitService()

