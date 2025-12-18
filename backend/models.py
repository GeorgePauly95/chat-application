from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import text, String, Text, Enum as SQLEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from services import is_empty
from engine import engine
from typing import Optional
from datetime import datetime
import uuid
import enum


def manage_connection(model_function):
    def inner(cls, *args, **kwargs):
        with engine.begin() as connection:
            return model_function(cls, connection, *args, **kwargs)

    return inner


class Base(DeclarativeBase):
    pass


class GroupMemberRole(enum.Enum):
    ADMIN = "admin"
    MEMBER = "member"


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("group_chats.id"))
    content: Mapped[str] = mapped_column(Text)
    sent_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=text("NOW()"))
    deleted_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)
    replied_to: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("messages.id"))

    @classmethod
    @manage_connection
    def showall_messages(cls, connection, group_id):
        messages = connection.execute(
            text("SELECT * FROM messages WHERE group_id=:group_id"),
            {"group_id": group_id},
        )
        mapped_messages = [message._mapping for message in messages.all()]
        return mapped_messages

    @classmethod
    @manage_connection
    def add_message(cls, connection, request_body):
        if is_empty(request_body["content"]):
            return None
        message = connection.execute(
            text(
                """INSERT INTO messages
        (sender_id, group_id, content) VALUES 
        (:sender_id, :group_id, :content) RETURNING *"""
            ),
            {
                "sender_id": request_body["sender_id"],
                "group_id": request_body["group_id"],
                "content": request_body["content"],
            },
        )
        sent_message = message.first()
        mapped_message = sent_message._mapping
        return mapped_message


class MessageStatus(Base):
    __tablename__ = "message_status"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    message_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("messages.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    read_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)


class UserAccount(Base):
    __tablename__ = "user_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_type: Mapped[str] = mapped_column(String(25))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    username: Mapped[str] = mapped_column(String(25))
    password: Mapped[str] = mapped_column(Text)

    @classmethod
    @manage_connection
    def get_user_details(cls, connection, username):
        user_accounts = connection.execute(
            text("SELECT * FROM user_accounts WHERE username=:username"),
            {"username": username},
        )
        user_account = user_accounts.first()
        if user_account is None:
            return user_account
        user_account_details = user_account._mapping
        return {
            "user_id": user_account_details["user_id"],
            "username": user_account_details["username"],
        }


class Group(Base):
    __tablename__ = "group_chats"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=text("NOW()")
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)

    @classmethod
    @manage_connection
    def showall_groups(cls, connection):
        messages = connection.execute(text("SELECT * FROM group_chats"))
        mapped_groups = [message._mapping for message in messages.all()]
        return mapped_groups

    @classmethod
    @manage_connection
    def add_group(cls, connection, request_body):
        group_details = connection.execute(
            text("INSERT INTO group_chats(name) VALUES(:name) RETURNING *"),
            {"name": request_body["name"]},
        ).first()
        group_details = dict(group_details._mapping)
        group_details["admin"] = request_body["admin"]
        group_details["members"] = request_body["members"]
        print(f"group result:{group_details}")
        GroupMember.add_groupmembers(connection, group_details)


class GroupMember(Base):
    __tablename__ = "group_members"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("group_chats.id"))
    role: Mapped[GroupMemberRole] = mapped_column(
        SQLEnum(GroupMemberRole, name="groupmemberrole")
    )
    joined_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=text("NOW()"))
    left_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)

    @classmethod
    def add_groupmembers(cls, connection, group_details):
        members = group_details["members"]
        admin = group_details["admin"]
        group_id = group_details["id"]
        connection.execute(
            text("""INSERT INTO group_members(user_id, group_id, role)
            VALUES(:user_id, :group_id, :role)"""),
            {
                "user_id": admin,
                "group_id": group_id,
                "role": GroupMemberRole.ADMIN,
            },
        )
        for member in members:
            connection.execute(
                text("""INSERT INTO group_members(user_id, group_id, role)
                VALUES(:user_id, :group_id, :role)"""),
                {
                    "user_id": member,
                    "group_id": group_id,
                    "role": GroupMemberRole.MEMBER,
                },
            )


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    token: Mapped[str] = mapped_column(Text)
    expires_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=text("NOW()")
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)

    @classmethod
    @manage_connection
    def show_users(cls, connection, user_id):
        users = connection.execute(
            text("SELECT * FROM users WHERE id!=:user_id"), {"user_id": user_id}
        )
        mapped_users = [user._mapping for user in users]
        return mapped_users
