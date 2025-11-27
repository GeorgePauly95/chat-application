from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


messages = [
    {
        "messageId": 1,
        "senderName": "George",
        "messageContent": "Hey",
        "sentAt": "12-12-2024",
        "readStatus": True,
        "repliedTo": None,
    },
    {
        "messageId": 2,
        "senderName": "George",
        "messageContent": "What's up",
        "sentAt": "12-12-2024",
        "readStatus": True,
        "repliedTo": None,
    },
]


@app.get("/api/messages")
async def show_messages():
    return messages


@app.post("/api/messages")
async def send_message(request: Request):
    json_body = await request.json()
    messages.append(json_body)
    return "message stored!"
