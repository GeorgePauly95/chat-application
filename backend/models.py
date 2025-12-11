from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import text, String, Text, Enum as SQLEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from typing import Optional
from datetime import datetime
import uuid
import enum


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
    def showall_messages(cls, user_id, connection):
        messages = connection.execute(
            text("SELECT * FROM messages WHERE sender_id=:user_id"),
            {"user_id": user_id},
        )
        mapped_messages = [message._mapping for message in messages.all()]
        return mapped_messages

    @classmethod
    def add_message(cls, request_body, connection):
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
        connection.commit()
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
    def get_user_details(cls, username, connection):
        user_accounts = connection.execute(
            text("SELECT * FROM user_accounts WHERE username=:username"),
            {"username": username},
        )
        user_accounts = user_accounts.first()
        return user_accounts


class Group(Base):
    __tablename__ = "group_chats"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)

    @classmethod
    def showall_groups(cls, connection):
        messages = connection.execute(text("SELECT * FROM group_chats"))
        mapped_groups = [message._mapping for message in messages.all()]
        return mapped_groups


class GroupMember(Base):
    __tablename__ = "group_members"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("group_chats.id"))
    role: Mapped[GroupMemberRole] = mapped_column(
        SQLEnum(GroupMemberRole, name="groupmemberrole")
    )
    joined_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    left_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)


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
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)
