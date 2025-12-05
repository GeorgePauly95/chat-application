from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text, Integer, Enum as SQLEnum, ForeignKey
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
    __tablename__ = "message"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    senderId: Mapped[int] = mapped_column(ForeignKey("user.id"))
    groupId: Mapped[int] = mapped_column(ForeignKey("group.id"))
    content: Mapped[str] = mapped_column(Text)
    sentAt: Mapped[datetime] = mapped_column(TIMESTAMP)
    deletedAt: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)
    repliedTo: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("message.id"))


class MessageStatus(Base):
    __tablename__ = "message_status"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    messageId: Mapped[uuid.UUID] = mapped_column(ForeignKey("message.id"))
    userId: Mapped[int] = mapped_column(ForeignKey("user.id"))
    readAt: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)


class UserAccount(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    accountType: Mapped[str] = mapped_column(String(25))
    userId: Mapped[int] = mapped_column(ForeignKey("user.id"))
    username: Mapped[str] = mapped_column(String(25))
    password: Mapped[str] = mapped_column(Text)


class Group(Base):
    __tablename__ = "group"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    createdAt: Mapped[datetime] = mapped_column(TIMESTAMP)
    deletedAt: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)


class GroupMember(Base):
    __tablename__ = "group_member"

    id: Mapped[int] = mapped_column(primary_key=True)
    userId: Mapped[int] = mapped_column(ForeignKey("user.id"))
    groupId: Mapped[int] = mapped_column(ForeignKey("group.id"))
    role: Mapped[GroupMemberRole] = mapped_column(
        SQLEnum(GroupMemberRole, name="groupmemberrole")
    )
    joinedAt: Mapped[datetime] = mapped_column(TIMESTAMP)
    leftAt: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)


class Session(Base):
    __tablename__ = "session"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    userId: Mapped[int] = mapped_column(ForeignKey("user.id"))
    token: Mapped[str] = mapped_column(Text)
    expiresAt: Mapped[datetime] = mapped_column(TIMESTAMP)
    createdAt: Mapped[datetime] = mapped_column(TIMESTAMP)
    deletedAt: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    createdAt: Mapped[datetime] = mapped_column(TIMESTAMP)
    deletedAt: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)
