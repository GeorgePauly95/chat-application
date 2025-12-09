from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import (
    User,
    Group,
    GroupMember,
    GroupMemberRole,
)
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
url = os.getenv("url")
engine = create_engine(f"{url}")
session = Session(engine)

user = User(id=1, name="Test User", created_at=datetime.now(), deleted_at=None)
session.add(user)

group = Group(id=1, name="Test Group", created_at=datetime.now(), deleted_at=None)
session.add(group)
session.flush()

group_member = GroupMember(
    user_id=1,
    group_id=1,
    role=GroupMemberRole.ADMIN,
    joined_at=datetime.now(),
    left_at=None,
)
session.add(group_member)

session.commit()
session.close()
