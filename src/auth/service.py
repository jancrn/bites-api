from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth as firebase_auth  # type:ignore[import]
from sqlalchemy.orm import Session

from auth import repository as auth_repository
from auth.exceptions import AuthenticationError
from auth.models import CreateUserRequest, FirebaseToken
from database import DbSession
from user import repository as user_repository
from user.models import User


async def get_current_user(
    db: DbSession,
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> User:
    try:
        decoded_token: FirebaseToken = firebase_auth.verify_id_token(  # type:ignore[no-untyped-call]
            credentials.credentials
        )
        if not decoded_token:
            raise AuthenticationError("Failed to decode token")

        email = decoded_token.get("email")  # type:ignore[no-untyped-call]

        user: User = user_repository.get_user_by_email(db, email)  # type:ignore[no-untyped-call]

        if not user:
            raise AuthenticationError("User not found")

        return user  # type:ignore[no-untyped-call]
    except Exception as e:
        print(e)
        raise AuthenticationError("Invalid token - Unknown error")


CurrentUser = Annotated[User, Depends(get_current_user)]


async def is_valid_token(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> bool:
    try:
        return firebase_auth.verify_id_token(credentials.credentials) is not None  # type:ignore[no-untyped-call]
    except Exception:
        return False


IsAuthenticated = Annotated[bool, Depends(is_valid_token)]


async def create_user(
    user: CreateUserRequest,
    db: Session,
) -> User:
    if not user.password:
        raise AuthenticationError("Password is required")
    if not user.email:
        raise AuthenticationError("Email is required")
    if not user.first_name:
        raise AuthenticationError("First name is required")
    if not user.last_name:
        raise AuthenticationError("Last name is required")
    user_exists = user_repository.get_user_by_email(db, user.email)
    if user_exists:
        raise AuthenticationError("User already exists")

    return auth_repository.create_user(
        db,
        id=user.firebase_uuid,
        token="",
        name=user.first_name + " " + user.last_name,
        email=user.email,
        email_verified_at=datetime.now(timezone.utc),
        password="",
        avatar="",
        type=1,
        open_id="",
        access_token="",
        deleted_at=None,
        phone=None,
        remember_token=None,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        device_token=None,
    )
