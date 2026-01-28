"""Tavus Persona API service for real-time digital human interactions"""
import httpx
import asyncio
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import logging

from app.config import settings

logger = logging.getLogger(__name__)


class TavusService:
    """Service for interacting with Tavus Persona API"""
    
    def __init__(self):
        self.api_key = settings.TAVUS_API_KEY
        self.persona_id = settings.TAVUS_PERSONA_ID
        self.base_url = settings.TAVUS_API_URL
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "x-api-key": self.api_key or "",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )
        self._conversations: Dict[str, Dict[str, Any]] = {}
    
    async def create_conversation(
        self,
        conversation_name: Optional[str] = None,
        custom_greeting: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a new Tavus conversation with the configured persona
        
        Args:
            conversation_name: Optional name for the conversation
            custom_greeting: Optional custom greeting message
            
        Returns:
            Dictionary containing conversation details including conversation_id
        """
        if not self.api_key or not self.persona_id:
            raise ValueError("Tavus API key and persona ID must be configured")
        
        try:
            payload = {
                "persona_id": self.persona_id,
                "conversation_name": conversation_name or f"conversation_{datetime.now().isoformat()}",
            }
            
            # Add conversational context if provided
            if custom_greeting:
                payload["conversational_context"] = custom_greeting
            
            logger.info(f"Creating Tavus conversation with persona {self.persona_id}")
            response = await self.client.post("/v2/conversations", json=payload)
            response.raise_for_status()
            
            data = response.json()
            conversation_id = data.get("conversation_id")
            
            # Store conversation metadata
            self._conversations[conversation_id] = {
                "id": conversation_id,
                "created_at": datetime.now().isoformat(),
                "status": "active",
                "metadata": data,
            }
            
            logger.info(f"Created Tavus conversation: {conversation_id}")
            return data
            
        except httpx.HTTPStatusError as e:
            logger.error(f"Tavus API error: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Failed to create Tavus conversation: {e.response.text}")
        except Exception as e:
            logger.error(f"Error creating Tavus conversation: {str(e)}")
            raise
    
    async def get_conversation_token(self, conversation_id: str) -> Dict[str, Any]:
        """
        Get connection details and token for a conversation
        
        Args:
            conversation_id: The Tavus conversation ID
            
        Returns:
            Dictionary containing connection URL and token
        """
        try:
            logger.info(f"Getting token for conversation: {conversation_id}")
            response = await self.client.get(f"/v2/conversations/{conversation_id}")
            response.raise_for_status()
            
            return response.json()
            
        except httpx.HTTPStatusError as e:
            logger.error(f"Tavus API error: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Failed to get conversation token: {e.response.text}")
        except Exception as e:
            logger.error(f"Error getting conversation token: {str(e)}")
            raise
    
    async def send_message(
        self,
        conversation_id: str,
        text: str,
    ) -> bool:
        """
        Send a text message to the avatar for TTS and lip-sync
        
        Note: In Tavus Persona API, messages are typically sent via WebRTC data channel
        after establishing the connection. This method is a placeholder for future
        implementation if Tavus adds a REST endpoint for message sending.
        
        Args:
            conversation_id: The Tavus conversation ID
            text: The message text to send
            
        Returns:
            True if successful
        """
        # For now, log the message
        # Actual message sending happens via LiveKit data channel
        logger.info(f"Message queued for conversation {conversation_id}: {text[:50]}...")
        
        if conversation_id in self._conversations:
            if "messages" not in self._conversations[conversation_id]:
                self._conversations[conversation_id]["messages"] = []
            self._conversations[conversation_id]["messages"].append({
                "text": text,
                "timestamp": datetime.now().isoformat(),
                "role": "user",
            })
        
        return True
    
    async def end_conversation(self, conversation_id: str) -> bool:
        """
        End a Tavus conversation and cleanup resources
        
        Args:
            conversation_id: The Tavus conversation ID
            
        Returns:
            True if successful
        """
        try:
            logger.info(f"Ending conversation: {conversation_id}")
            
            # Update local metadata
            if conversation_id in self._conversations:
                self._conversations[conversation_id]["status"] = "ended"
                self._conversations[conversation_id]["ended_at"] = datetime.now().isoformat()
            
            # Tavus conversations typically end when the WebRTC connection closes
            # No explicit API call needed, but we can optionally call DELETE if needed
            try:
                response = await self.client.delete(f"/v2/conversations/{conversation_id}")
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                # It's okay if this fails - conversation might already be ended
                logger.warning(f"Could not delete conversation {conversation_id}: {e.response.text}")
            
            logger.info(f"Conversation ended: {conversation_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error ending conversation: {str(e)}")
            return False
    
    async def get_conversation_status(self, conversation_id: str) -> Dict[str, Any]:
        """
        Get the status of a conversation
        
        Args:
            conversation_id: The Tavus conversation ID
            
        Returns:
            Dictionary containing conversation status and metadata
        """
        try:
            # First check local cache
            if conversation_id in self._conversations:
                local_data = self._conversations[conversation_id]
            else:
                local_data = {"id": conversation_id, "status": "unknown"}
            
            # Get latest from API
            try:
                response = await self.client.get(f"/v2/conversations/{conversation_id}")
                response.raise_for_status()
                api_data = response.json()
                
                # Merge with local data
                return {
                    **local_data,
                    **api_data,
                }
            except httpx.HTTPStatusError:
                # Conversation might not exist anymore
                return local_data
            
        except Exception as e:
            logger.error(f"Error getting conversation status: {str(e)}")
            raise
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


# Singleton instance
_tavus_service: Optional[TavusService] = None


def get_tavus_service() -> TavusService:
    """Get or create the Tavus service singleton"""
    global _tavus_service
    if _tavus_service is None:
        _tavus_service = TavusService()
    return _tavus_service
