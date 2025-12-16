from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from engine import engine
from models import Message, Group, UserAccount, User

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


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


@app.get("/api/groups")
async def show_groups():
    return Group.showall_groups()


@app.post("/api/login")
async def login(request: Request):
    request_body = await request.json()
    username = request_body["username"]
    user_details = UserAccount.get_user_details(username)
    if user_details is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Unauthorized"},
        )
    return user_details


@app.get("/api/users")
async def show_users():
    return User.show_users()
