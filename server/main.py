from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from datetime import datetime
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from server.database import (
    save_message,
    get_chat_history,
    update_message,
    delete_message
)
from server.connection_manager import ConnectionManager
from server.auth import verify_token, create_token

app = FastAPI()
manager = ConnectionManager()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def get_ui():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.post("/login/{username}")
def login(username: str):
    return {"token": create_token(username)}


@app.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    username = verify_token(token)
    if not username:
        await websocket.close(code=1008)
        return

    # ✅ ACCEPT CONNECTION
    await websocket.accept()

    # ✅ REGISTER USER
    manager.active_connections[username] = websocket

    # ✅ JOIN MESSAGE + USERS
    await manager.broadcast(f"__system__:🟢 {username} joined the chat")
    await manager.broadcast_users()

    # ✅ SEND CHAT HISTORY (ONE FORMAT ONLY)
    history = get_chat_history()
    for msg_id, u, m, t, d, edited in history:
        edited_flag = " (edited)" if edited else ""
        await websocket.send_text(
            f"{msg_id}|{u}|{m}{edited_flag}|{t}|{d}"
        )

    try:
        while True:
            message = await websocket.receive_text()

            # 🟣 SEEN
            if message.startswith("__seen__:"):
                msg_id = int(message.replace("__seen__:", ""))
                await manager.broadcast(f"__seen__:{msg_id}")
                continue

            # 🟣 TYPING
            if message in ("__typing__", "__stop__"):
                await manager.broadcast(f"{message}:{username}")
                continue

            # 🟣 EDIT
            if message.startswith("__edit__:"):
                msg_id, new_text = message.replace("__edit__:", "").split("|", 1)
                update_message(int(msg_id), new_text)
                await manager.broadcast(f"__edit__:{msg_id}|{new_text}")
                continue

            # 🟣 DELETE
            if message.startswith("__delete__:"):
                msg_id = message.replace("__delete__:", "")
                delete_message(int(msg_id))
                await manager.broadcast(f"__delete__:{msg_id}")
                continue

            # 🟢 REAL CHAT MESSAGE
            timestamp = datetime.now().strftime("%H:%M")
            date = datetime.now().strftime("%Y-%m-%d")

            msg_id, timestamp, date = save_message(username, message)

            await manager.broadcast(
                f"{msg_id}|{username}|{message}|{timestamp}|{date}"
            )

            print("📨 sending:", f"{username}|{message}|{timestamp}")

    except WebSocketDisconnect:
        manager.active_connections.pop(username, None)

        try:
            await manager.broadcast(f"__system__:🔴 {username} left the chat")
            await manager.broadcast_users()
        except:
            pass
