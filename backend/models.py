from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import text, String, Text, Enum as SQLEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from services import is_empty
from engine import engine
from typing import Optional
from datetime import datetime
import uuid
import enum


# do a conditional check on connection for None so that functions like add_group_members can be called independently. make it a kwarg.
def manage_connection(model_function):
    def inner(cls, *args, **kwargs):
        with engine.begin() as connection:
            return model_function(cls, connection, *args, **kwargs)

    return inner


class Base(DeclarativeBase):
    pass


# str ENUM
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
    # change "request_body" to "message"
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
    salt: Mapped[str] = mapped_column(Text)

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
        return user_account_details

    @classmethod
    @manage_connection
    def register_user(cls, connection, user_id, username, password, salt):
        account_type = "normal"
        user_details = connection.execute(
            text("""INSERT INTO user_accounts(account_type, user_id, username, password, salt)
            VALUES(:account_type, :user_id, :username, :password, :salt) RETURNING *"""),
            {
                "account_type": account_type,
                "user_id": user_id,
                "username": username,
                "password": password,
                "salt": salt,
            },
        )
        return user_details


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
    def showall_groups(cls, connection, user_id):
        group_ids = connection.execute(
            text("SELECT group_id FROM group_members WHERE user_id=:user_id"),
            {"user_id": user_id},
        )
        group_ids = [group_id._mapping["group_id"] for group_id in group_ids]

        groups = connection.execute(
            text("SELECT * FROM group_chats WHERE id = ANY(:group_ids)"),
            {"group_ids": group_ids},
        )

        groups = [group._mapping for group in groups.all()]
        return groups

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

    # make this a part of add_group method itself.
    @classmethod
    def add_groupmembers(cls, connection, group_details):
        members = group_details["members"]
        admin = group_details["admin"]
        group_id = group_details["id"]
        # combine this query with the one below
        connection.execute(
            text("""INSERT INTO group_members(user_id, group_id, role)
            VALUES(:user_id, :group_id, :role)"""),
            {
                "user_id": admin,
                "group_id": group_id,
                "role": GroupMemberRole.ADMIN,
            },
        )
        # use an array to insert values instead of a for loop
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

    @classmethod
    @manage_connection
    def add_user(cls, connection, username):
        created_user = connection.execute(
            text("INSERT INTO users(name) VALUES(:name) RETURNING *"),
            {"name": username},
        ).first()
        created_user = created_user._mapping
        return created_user
