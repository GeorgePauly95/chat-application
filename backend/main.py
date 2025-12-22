from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
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
