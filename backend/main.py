from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from engine import engine
from models import Message, Group, UserAccount
from services import get_user_details

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/messages/")
async def show_messages(userid: int):
    connection = engine.connect()
    return Message.showall_messages(userid, connection)


@app.post("/api/messages")
async def send_message(request: Request):
    request_body = await request.json()
    connection = engine.connect()
    return Message.add_message(request_body, connection)


@app.get("/api/groups")
async def show_groups():
    connection = engine.connect()
    return Group.showall_groups(connection)


@app.post("/api/login")
async def login(request: Request):
    request_body = await request.json()
    connection = engine.connect()
    username = request_body["username"]
    user_details = get_user_details(username, UserAccount, connection)
    if not user_details:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Unauthorized"},
        )
    return user_details
