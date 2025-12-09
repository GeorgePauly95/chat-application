from fastapi import FastAPI, Request
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()
url = os.getenv("url")
engine = create_engine(f"{url}", echo=True)
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/messages")
async def show_messages():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM messages"))
        messages = result.all()
        conn.commit()
    messages = [dict(message._mapping) for message in messages]
    return messages


@app.post("/api/messages")
async def send_message(request: Request):
    json_body = await request.json()
    with engine.connect() as conn:
        conn.execute(
            text(
                """INSERT INTO messages
        (id, sender_id, group_id, content, sent_at, deleted_at, replied_to) VALUES 
        (:id, :sender_id, :group_id, :content, :sent_at, :deleted_at, :replied_to)"""
            ),
            {
                "id": json_body["id"],
                "sender_id": json_body["sender_id"],
                "group_id": json_body["group_id"],
                "content": json_body["content"],
                "sent_at": json_body["sent_at"],
                "deleted_at": json_body["deleted_at"],
                "replied_to": json_body["replied_to"],
            },
        )
        conn.commit()
    return "message stored!"


@app.get("/api/groups")
async def show_groups():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM group_chats"))
        groups = result.all()
        conn.commit()
    groups = [group._mapping for group in groups]
    return groups
