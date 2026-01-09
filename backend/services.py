from fastapi import WebSocket
from fastapi.encoders import jsonable_encoder
from models import Message, GroupMember


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    async def create_connection(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections.update({user_id: websocket})

    def get_connection(self, user_id: int):
        connection = self.active_connections.get(user_id)
        return connection

    def remove_connection(self, user_id: int):
        websocket = self.active_connections.pop(user_id)
        if websocket:
            websocket.close()

    async def send_message(self, message, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast_message_to_group(self, sender_id: int, message_content):
        message = Message.add_message(message_content)
        group_id = message["group_id"]
        encoded_message = jsonable_encoder(message)
        member_ids = GroupMember.showall_groupmembers(group_id)
        for member_id in member_ids:
            member_connection = self.get_connection(member_id)
            if member_connection is None:
                continue
            await self.send_message(encoded_message, member_connection)
