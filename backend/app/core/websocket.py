from fastapi import WebSocket, WebSocketDisconnect, Depends
from typing import Dict, Set
import json
import asyncio


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.rooms: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room: str = "public"):
        await websocket.accept()
        if room not in self.active_connections:
            self.active_connections[room] = set()
        self.active_connections[room].add(websocket)

    def disconnect(self, websocket: WebSocket, room: str = "public"):
        if room in self.active_connections:
            self.active_connections[room].discard(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(json.dumps({"type": "personal", "data": message}))

    async def broadcast(self, message: dict, room: str = "public"):
        if room not in self.active_connections:
            return
        for connection in self.active_connections[room]:
            try:
                await connection.send_text(json.dumps(message))
            except:
                pass


manager = ConnectionManager()