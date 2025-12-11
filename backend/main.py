from fastapi import FastAPI, Request
from engine import engine
from models import Message, Group, UserAccount
from services import check_user

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/messages")
async def show_messages():
    connection = engine.connect()
    return Message.showall_messages(connection)


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
    return check_user(username, UserAccount, connection)
