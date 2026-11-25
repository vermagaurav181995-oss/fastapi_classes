from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()


class ConnectionManager:

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict) -> None:
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()


@router.websocket("/ws/chat/{username}")
async def chat(websocket: WebSocket, username: str):
    await manager.connect(websocket)
    await manager.broadcast({"user": "system", "message": f"{username} joined the chat"})
    try:
        while True:
            text = await websocket.receive_text()
            await manager.broadcast({"user": username, "message": text})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast({"user": "system", "message": f"{username} left the chat"})
