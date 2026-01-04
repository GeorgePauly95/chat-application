from fastapi import FastAPI, Request, status, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import json
from models import Message, Group, UserAccount, User, GroupMember
from services import (
    ConnectionManager,
)

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
            message = Message.add_message(data)
            group_id = message["group_id"]
            encoded_message = jsonable_encoder(message)
            group_member_ids = GroupMember.showall_groupmembers(group_id)
            for group_member_id in group_member_ids:
                if user_id == group_member_id:
                    continue
                else:
                    member_connection = connection_manager.get_connection(
                        group_member_id
                    )
                    if member_connection is None:
                        continue
                    await connection_manager.send_message(
                        encoded_message, member_connection
                    )
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
