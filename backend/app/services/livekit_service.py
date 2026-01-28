"""LiveKit service for real-time audio/video streaming"""
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from livekit.api import AccessToken, VideoGrants, LiveKitAPI
from livekit.api import CreateRoomRequest, DeleteRoomRequest, ListRoomsRequest

from app.config import settings

logger = logging.getLogger(__name__)


class LiveKitService:
    """Service for managing LiveKit rooms and tokens"""
    
    def __init__(self):
        self.api_key = settings.LIVEKIT_API_KEY
        self.api_secret = settings.LIVEKIT_API_SECRET
        self.url = settings.LIVEKIT_URL
        
        if self.api_key and self.api_secret and self.url:
            self.livekit_api = LiveKitAPI(
                self.url,
                self.api_key,
                self.api_secret,
            )
        else:
            self.livekit_api = None
            logger.warning("LiveKit credentials not configured")
    
    async def create_room(
        self,
        room_name: str,
        empty_timeout: int = 300,  # 5 minutes
        max_participants: int = 10,
    ) -> Dict[str, Any]:
        """
        Create a LiveKit room with optimized settings for avatar streaming
        
        Args:
            room_name: Unique name for the room
            empty_timeout: Timeout in seconds before room closes when empty
            max_participants: Maximum number of participants
            
        Returns:
            Dictionary containing room details
        """
        if not self.livekit_api:
            raise ValueError("LiveKit is not configured")
        
        try:
            logger.info(f"Creating LiveKit room: {room_name}")
            
            room = await self.livekit_api.room.create_room(
                CreateRoomRequest(
                    name=room_name,
                    empty_timeout=empty_timeout,
                    max_participants=max_participants,
                )
            )
            
            logger.info(f"Created LiveKit room: {room.name} (SID: {room.sid})")
            
            return {
                "name": room.name,
                "sid": room.sid,
                "creation_time": room.creation_time,
                "num_participants": room.num_participants,
            }
            
        except Exception as e:
            logger.error(f"Error creating LiveKit room: {str(e)}")
            raise
    
    def generate_token(
        self,
        room_name: str,
        participant_identity: str,
        participant_name: Optional[str] = None,
        can_publish: bool = True,
        can_subscribe: bool = True,
        can_publish_data: bool = True,
        token_ttl: int = 3600,  # 1 hour
    ) -> str:
        """
        Generate a LiveKit access token for a participant
        
        Args:
            room_name: Name of the room to join
            participant_identity: Unique identity for the participant
            participant_name: Display name for the participant
            can_publish: Whether participant can publish tracks
            can_subscribe: Whether participant can subscribe to tracks
            can_publish_data: Whether participant can publish data messages
            token_ttl: Token time-to-live in seconds
            
        Returns:
            JWT token string
        """
        if not self.api_key or not self.api_secret:
            raise ValueError("LiveKit API credentials not configured")
        
        try:
            logger.info(f"Generating token for {participant_identity} in room {room_name}")
            
            token = AccessToken(self.api_key, self.api_secret)
            token.identity = participant_identity
            token.name = participant_name or participant_identity
            
            # Set video grants
            grants = VideoGrants(
                room_join=True,
                room=room_name,
                can_publish=can_publish,
                can_subscribe=can_subscribe,
                can_publish_data=can_publish_data,
            )
            token.video_grants = grants
            
            # Set token expiration
            token.ttl = timedelta(seconds=token_ttl)
            
            jwt_token = token.to_jwt()
            logger.info(f"Generated token for {participant_identity}")
            
            return jwt_token
            
        except Exception as e:
            logger.error(f"Error generating LiveKit token: {str(e)}")
            raise
    
    async def delete_room(self, room_name: str) -> bool:
        """
        Delete a LiveKit room
        
        Args:
            room_name: Name of the room to delete
            
        Returns:
            True if successful
        """
        if not self.livekit_api:
            raise ValueError("LiveKit is not configured")
        
        try:
            logger.info(f"Deleting LiveKit room: {room_name}")
            
            await self.livekit_api.room.delete_room(
                DeleteRoomRequest(room=room_name)
            )
            
            logger.info(f"Deleted LiveKit room: {room_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting LiveKit room: {str(e)}")
            return False
    
    async def list_rooms(self) -> list[Dict[str, Any]]:
        """
        List all active LiveKit rooms
        
        Returns:
            List of room dictionaries
        """
        if not self.livekit_api:
            raise ValueError("LiveKit is not configured")
        
        try:
            rooms = await self.livekit_api.room.list_rooms(ListRoomsRequest())
            
            return [
                {
                    "name": room.name,
                    "sid": room.sid,
                    "num_participants": room.num_participants,
                    "creation_time": room.creation_time,
                }
                for room in rooms.rooms
            ]
            
        except Exception as e:
            logger.error(f"Error listing LiveKit rooms: {str(e)}")
            raise
    
    async def get_room(self, room_name: str) -> Optional[Dict[str, Any]]:
        """
        Get details of a specific room
        
        Args:
            room_name: Name of the room
            
        Returns:
            Room details dictionary or None if not found
        """
        if not self.room_service:
            raise ValueError("LiveKit is not configured")
        
        try:
            rooms = await self.list_rooms()
            for room in rooms:
                if room["name"] == room_name:
                    return room
            return None
            
        except Exception as e:
            logger.error(f"Error getting room: {str(e)}")
            return None


# Singleton instance
_livekit_service: Optional[LiveKitService] = None


def get_livekit_service() -> LiveKitService:
    """Get or create the LiveKit service singleton"""
    global _livekit_service
    if _livekit_service is None:
        _livekit_service = LiveKitService()
    return _livekit_service
