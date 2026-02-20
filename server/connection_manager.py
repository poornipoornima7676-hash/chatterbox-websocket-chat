from fastapi import WebSocket
from typing import Dict

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, username: str, websocket: WebSocket):
        await websocket.accept()    
        self.active_connections[username] = websocket

    def disconnect(self, username: str):
        self.active_connections.pop(username, None)

    async def broadcast(self, message: str):
        for ws in self.active_connections.values():
            await ws.send_text(message)

    async def broadcast(self, message: str):
        disconnected = []

        for username, ws in self.active_connections.items():
            try:
                await ws.send_text(message)
            except Exception:
                disconnected.append(username)

    # cleanup dead sockets
        for username in disconnected:
            self.active_connections.pop(username, None)

    async def broadcast_users(self):
        users = ",".join(self.active_connections.keys())

        disconnected = []
        for username, ws in self.active_connections.items():
            try:
                await ws.send_text(f"__users__:{users}")
            except Exception:
                disconnected.append(username)

        for username in disconnected:
            self.active_connections.pop(username, None)
        
