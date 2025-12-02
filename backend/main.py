from fastapi import FastAPI, Request

app = FastAPI()

messages = []

groups = [
    {
        "id": 1,
        "name": "Bit by Bit",
        "createdAt": "12-12-2025",
        "deletedAt": None,
    },
    {
        "id": 2,
        "name": "Aaqib",
        "createdAt": "12-12-2025",
        "deletedAt": None,
    },
]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/messages")
async def show_messages():
    return messages


@app.post("/api/messages")
async def send_message(request: Request):
    json_body = await request.json()
    messages.append(json_body)
    return "message stored!"


@app.get("/api/groups")
async def show_groups():
    return groups
