"""Tavus Persona API service"""
import httpx
import logging
from typing import Optional, Dict, Any
import uuid

from app.config import settings

logger = logging.getLogger(__name__)


class TavusService:
    """Service for interacting with Tavus Persona API"""
    
    def __init__(self):
        self.api_key = settings.TAVUS_API_KEY
        self.api_url = settings.TAVUS_API_URL
        self.persona_id = settings.TAVUS_PERSONA_ID
        self.client = httpx.AsyncClient(
            base_url=self.api_url,
            headers={
                "x-api-key": self.api_key or "",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )
    
    async def generate_avatar(
        self,
        text: str,
        persona_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate avatar video from text using Tavus Persona API
        
        Args:
            text: Text to convert to speech
            persona_id: Optional persona ID (uses default if not provided)
        
        Returns:
            Dictionary with session_id and status
        """
        if not self.api_key:
            logger.warning("Tavus API key not configured, using mock response")
            return self._mock_generate(text)
        
        try:
            persona = persona_id or self.persona_id
            if not persona:
                raise ValueError("Persona ID is required")
            
            # Generate a unique session ID
            session_id = str(uuid.uuid4())
            
            # Call Tavus API to create a replica video
            # Note: This is a simplified example - actual Tavus API may differ
            payload = {
                "persona_id": persona,
                "script": text,
                "callback_url": None,  # Could set up webhook URL here
            }
            
            response = await self.client.post(
                "/v2/replicas",
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            
            return {
                "session_id": session_id,
                "tavus_replica_id": result.get("replica_id"),
                "status": "generating",
                "video_url": None,
            }
            
        except httpx.HTTPError as e:
            logger.error(f"Tavus API error: {e}")
            # Fallback to mock for development
            return self._mock_generate(text)
        except Exception as e:
            logger.error(f"Error generating avatar: {e}")
            raise
    
    async def get_replica_status(self, replica_id: str) -> Dict[str, Any]:
        """
        Get status of a Tavus replica generation
        
        Args:
            replica_id: Tavus replica ID
        
        Returns:
            Dictionary with status and video URL if ready
        """
        if not self.api_key:
            return {
                "status": "ready",
                "video_url": "https://example.com/mock-video.mp4",
            }
        
        try:
            response = await self.client.get(f"/v2/replicas/{replica_id}")
            response.raise_for_status()
            
            result = response.json()
            
            return {
                "status": result.get("status", "unknown"),
                "video_url": result.get("video_url"),
                "audio_url": result.get("audio_url"),
            }
        except httpx.HTTPError as e:
            logger.error(f"Error fetching replica status: {e}")
            return {"status": "error", "error": str(e)}
    
    def _mock_generate(self, text: str) -> Dict[str, Any]:
        """Mock generation for development/testing"""
        session_id = str(uuid.uuid4())
        logger.info(f"Mock avatar generation for text: {text[:50]}...")
        return {
            "session_id": session_id,
            "tavus_replica_id": f"mock_{session_id}",
            "status": "generating",
            "video_url": None,
        }
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


# Global instance
tavus_service = TavusService()

