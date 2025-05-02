from datetime import datetime

from sqlalchemy import TIMESTAMP
from sqlmodel import Field, SQLModel


class User(
    SQLModel,
    table=True,
):
    id: str | None = Field(default=None, primary_key=True)

    token: str = Field(max_length=100, nullable=False)
    name: str = Field(max_length=255, nullable=False)
    email: str = Field(max_length=255, nullable=False, unique=True)

    email_verified_at: datetime | None = Field(sa_type=TIMESTAMP, default=None)
    password: str | None = Field(max_length=255, default=None)

    avatar: str = Field(max_length=100, nullable=False)
    type: int = Field(nullable=False)
    open_id: str = Field(max_length=80, nullable=False)
    access_token: str | None = Field(max_length=80, default=None)

    # deleted_at: datetime = Field( sa_type=TIMESTAMP, default_factory=func.current_timestamp )
    deleted_at: datetime | None = Field(sa_type=TIMESTAMP, default=None)

    phone: str | None = Field(max_length=20, default=None)
    remember_token: str | None = Field(max_length=100, default=None)
    created_at: datetime | None = Field(sa_type=TIMESTAMP, default=None)
    updated_at: datetime | None = Field(sa_type=TIMESTAMP, default=None)
    device_token: str | None = Field(max_length=255, default=None)
