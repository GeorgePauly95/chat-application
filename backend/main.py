from fastapi import FastAPI, Request, status, WebSocket
from fastapi.responses import JSONResponse
from models import Message, Group, UserAccount, User
import json

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.websocket("/api/messages")
async def websocket_endpoint(websocket: WebSocket):
    group_id = websocket.query_params.get("group_id")
    await websocket.accept()
    while True:
        text_data = await websocket.receive_text()
        data = json.loads(text_data)
        Message.add_message(data)
        await websocket.send_text(json.dumps(Message.showall_messages(group_id)))


# @app.get("/api/messages")
# async def show_messages_by_user(user_id: int):
#     # groups = Group.showall_groups(user_id)
#
#     return


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
