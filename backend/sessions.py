from fastapi import Request, Response, status, HTTPException, Cookie
from typing import Annotated
from utils import create_session_id
from datetime import datetime, timedelta
from engine import redis_conn
import json


def get_session_id(request: Request):
    print(f"REQUEST IS: {request}")
    return request.cookies.get("session_id")


def create_session(redis_conn, user_id, response: Response):
    session_id = create_session_id()
    expires_at = datetime.now() + timedelta(minutes=1)
    session_data = {"user_id": user_id, "expires": expires_at.isoformat()}
    redis_conn.set(session_id, json.dumps(session_data))
    response.set_cookie(
        key="session_id", value=session_id, Httponly=True, Expires=expires_at
    )
    return session_id


def validate_session(request: Request, redis_conn):
    session_id = request.cookies.get("session_id")
    print(f"SESSION ID: {session_id}")
    if session_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Please Login"
        )
    session_data = redis_conn.get(session_id)
    if session_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Please Login"
        )
    session_data = json.loads(session_data)
    expires_at = session_data.get("expires")
    expires_at = datetime.fromisoformat(expires_at)
    current_time = datetime.now()
    if current_time > expires_at:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Please Login"
        )
    return session_data
