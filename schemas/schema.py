import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import UUID

from config import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4(),
        index=True,
        unique=True,
        nullable=False,
    )
    email = Column(
        String(),
        unique=True,
        nullable=False,
        index=True,
    )
    username = Column(String(), nullable=False)
    password = Column(String(), nullable=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(), default=datetime.now(), nullable=False)

    # relation to urls: 1 -> M

    urls = relationship("Urls", back_populates="user", cascade="all, delete-orphan")


class Urls(Base):
    __tablename__ = "urls"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4(),
        index=True,
        unique=True,
        nullable=False,
    )
    original_url = Column(String(), nullable=False)
    short_url = Column(String(), nullable=False, index=True)
    created_at = Column(DateTime(), default=datetime.now(), nullable=False)

    # connects back to user: M -> 1

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"),
    )
    user = relationship("users", back_populates="urls")

    # relation to url_logs: 1 -> M

    url_logs = relationship(
        "url_logs", back_populates="urls", cascade="all, delete-orphan"
    )


class UrlLogs(Base):
    __tablename__ = "url_logs"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4(),
        index=True,
        unique=True,
        nullable=False,
    )
    requested_url = Column(String(), nullable=False)
    requested_by = Column(String(), nullable=False)
    total_requests = Column(String(), nullable=False)
    requested_at = Column(DateTime(), default=datetime.now(), nullable=False)

    url_id = Column(
        UUID(as_uuid=True),
        ForeignKey("urls.id", onupdate="CASCADE", ondelete="CASCADE"),
    )
    url = relationship("urls", back_populates="url_logs", cascade="all, delete-orphan")
