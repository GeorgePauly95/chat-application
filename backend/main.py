from fastapi import Depends, FastAPI, Request, status, WebSocket
from fastapi.responses import JSONResponse
from models import Message, Group, UserAccount, User
import bcrypt

app = FastAPI()


async def session_authentication():
    return


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(data)


@app.get("/api/messages/")
async def show_messages(groupid: int):
    return Message.showall_messages(groupid)


@app.post("/api/messages")
async def send_message(request: Request):
    request_body = await request.json()
    response = Message.add_message(request_body)
    if response is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={})
    return response


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
