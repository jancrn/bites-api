from datetime import datetime
from uuid import UUID

from database import DbSession
from user.models import User


def create_user(
    db: DbSession,
    id: UUID,
    token: str,
    name: str,
    email: str,
    email_verified_at: datetime | None,
    password: str | None,
    avatar: str,
    type: int,
    open_id: str,
    access_token: str | None,
    deleted_at: datetime | None,
    phone: str | None,
    remember_token: str | None,
    created_at: datetime | None,
    updated_at: datetime | None,
    device_token: str | None,
) -> User:
    db_user = User(
        id=id,
        token=token,
        name=name,
        email=email,
        email_verified_at=email_verified_at,
        password=password,
        avatar=avatar,
        type=type,
        open_id=open_id,
        access_token=access_token,
        deleted_at=deleted_at,
        phone=phone,
        remember_token=remember_token,
        created_at=created_at,
        updated_at=updated_at,
        device_token=device_token,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
