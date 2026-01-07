from fastapi import FastAPI, Request, Response, status, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from models import Group, UserAccount, User
from services import ConnectionManager
from sessions import create_session, validate_session
from engine import redis_conn
import bcrypt
import json

app = FastAPI()
connection_manager = ConnectionManager()


@app.get("/api/me")
async def check_session(request: Request):
    session_data = validate_session(request, redis_conn)
    return session_data


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
async def login(request: Request, response: Response):
    request_body = await request.json()
    username, password = request_body["username"], request_body["password"]
    user_details = UserAccount.get_user_details(username)
    if user_details is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={},
        )
    else:
        stored_password, salt = user_details["password"], user_details["salt"]
        encoded_stored_password, encoded_salt = (
            stored_password.encode("utf-8"),
            salt.encode("utf-8"),
        )
        calc_password = bcrypt.hashpw(password.encode("utf-8"), encoded_salt)

        if calc_password == encoded_stored_password:
            user_id = user_details["user_id"]
            create_session(redis_conn, user_id, response)
            return user_details
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={},
        )


@app.post("/api/register")
async def register(request: Request):
    request_body = await request.json()
    username, password = request_body["username"], request_body["password"]
    created_user = User.add_user(username)
    user_id = created_user["id"]
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    decoded_hashed_password, decoded_salt = (
        hashed_password.decode("utf-8"),
        salt.decode("utf-8"),
    )
    user_details = UserAccount.register_user(
        user_id, username, decoded_hashed_password, decoded_salt
    ).first()
    user_details = user_details._mapping
    return user_details


@app.get("/api/users/{user_id}")
async def show_users(user_id):
    return User.show_users(user_id)
