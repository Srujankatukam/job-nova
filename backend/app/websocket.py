"""WebSocket handlers for real-time communication"""
from fastapi import WebSocket, WebSocketDisconnect
import logging
import json
from typing import Dict, Set
import asyncio

from app.services.tavus_service import tavus_service
from app.services.livekit_service import livekit_service

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.session_data: Dict[str, Dict] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        """Accept WebSocket connection and add to active connections"""
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = set()
        self.active_connections[session_id].add(websocket)
        logger.info(f"WebSocket connected for session {session_id}")
    
    def disconnect(self, websocket: WebSocket, session_id: str):
        """Remove WebSocket from active connections"""
        if session_id in self.active_connections:
            self.active_connections[session_id].discard(websocket)
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]
        logger.info(f"WebSocket disconnected for session {session_id}")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send message to a specific WebSocket connection"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending message: {e}")
    
    async def broadcast_to_session(self, session_id: str, message: dict):
        """Broadcast message to all connections in a session"""
        if session_id in self.active_connections:
            disconnected = set()
            for connection in self.active_connections[session_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error broadcasting to session {session_id}: {e}")
                    disconnected.add(connection)
            
            # Remove disconnected connections
            for conn in disconnected:
                self.disconnect(conn, session_id)


# Global connection manager
manager = ConnectionManager()


async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for avatar session updates
    
    Args:
        websocket: WebSocket connection
        session_id: Avatar session ID
    """
    await manager.connect(websocket, session_id)
    
    try:
        # Send initial connection confirmation
        await manager.send_personal_message(
            {
                "type": "connected",
                "sessionId": session_id,
                "message": "WebSocket connected",
            },
            websocket
        )
        
        # Listen for messages from client
        while True:
            try:
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Handle different message types
                if message.get("type") == "status_request":
                    # Client requesting status update
                    if session_id in manager.session_data:
                        await manager.send_personal_message(
                            {
                                "type": "status",
                                "sessionId": session_id,
                                "data": manager.session_data[session_id],
                            },
                            websocket
                        )
                
            except WebSocketDisconnect:
                break
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON received from session {session_id}")
            except Exception as e:
                logger.error(f"Error handling WebSocket message: {e}")
                await manager.send_personal_message(
                    {
                        "type": "error",
                        "sessionId": session_id,
                        "message": str(e),
                    },
                    websocket
                )
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)
    except Exception as e:
        logger.error(f"WebSocket error for session {session_id}: {e}")
        manager.disconnect(websocket, session_id)


async def update_session_status(session_id: str, status: str, data: Dict = None):
    """
    Update session status and broadcast to all connected clients
    
    Args:
        session_id: Session ID
        status: Status string (pending, generating, ready, error)
        data: Additional data to include
    """
    update_data = {
        "type": "status",
        "sessionId": session_id,
        "status": status,
        "data": data or {},
    }
    
    # Store session data
    manager.session_data[session_id] = {
        "status": status,
        **update_data.get("data", {}),
    }
    
    # Broadcast to all connections in this session
    await manager.broadcast_to_session(session_id, update_data)

