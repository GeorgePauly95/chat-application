from fastapi import WebSocket


class ConnectionManager(dict):
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    async def create_connection(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections.update({user_id: websocket})

    def get_connection(self, user_id: int):
        connection = self.active_connections.get(user_id)
        return connection

    async def send_message(self, message, websocket: WebSocket):
        await websocket.send_json(message)

    def remove_connection(self, user_id: int):
        del self.active_connections[user_id]


def is_empty(text):
    cleaned_text = text.strip()
    if cleaned_text == "":
        return True
    return False
