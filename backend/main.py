from fastapi import FastAPI, Request, status, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
import json
from models import Group, UserAccount, User
from services import ConnectionManager

app = FastAPI()
connection_manager = ConnectionManager()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.websocket("/api/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await connection_manager.create_connection(websocket, user_id)
    try:
        while True:
            text_data = await websocket.receive_text()
            data = json.loads(text_data)
            await connection_manager.broadcast_message_to_group(user_id, data)
    except WebSocketDisconnect:
        connection_manager.remove_connection(user_id)


@app.get("/api/groups/")
async def show_groups(user_id: int):
    groups = Group.showall_groups(user_id)
    return groups


@app.post("/api/groups")
async def create_group(request: Request):
    request_body = await request.json()
    Group.add_group(request_body)
    return "GROUP CREATED!"


@app.post("/api/login")
async def login(request: Request):
    request_body = await request.json()
    username = request_body["username"]
    user_details = UserAccount.get_user_details(username)
    if user_details is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={},
        )
    return user_details


@app.get("/api/users/{user_id}")
async def show_users(user_id):
    return User.show_users(user_id)
