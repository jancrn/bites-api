import logging
from datetime import datetime, timedelta, timezone
from typing import Annotated
from uuid import UUID

import jwt
from fastapi import Depends
from jwt import PyJWTError
from sqlalchemy.orm import Session

import env
from auth import repository as auth_repository
from auth.config import bcrypt_context, oauth2_bearer
from auth.exceptions import AuthenticationError
from auth.models import SignInUserRequest, SignUpUserRequest, Token, TokenData
from user import repository as user_repository
from user.models import User


def signup(user: SignUpUserRequest, db: Session) -> User:
    return auth_repository.create_user(
        db,
        id=UUID(),
        token="",
        name=user.first_name + " " + user.last_name,
        email=user.email,
        email_verified_at=datetime.now(timezone.utc),
        password=bcrypt_context.hash(user.password),  # Get Password Hash
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


def create_access_token(email: str, user_id: UUID, expires_delta: timedelta) -> str:
    return jwt.encode(
        {
            "sub": email,
            "id": str(user_id),
            "exp": datetime.now(timezone.utc) + expires_delta,
        },
        env.get("SECRET_KEY"),
        env.get("ALGORITHM"),
    )


def signin(form_data: SignInUserRequest, db: Session) -> Token:
    user = user_repository.get_user_by_email(db, form_data.username)
    if not user:
        raise AuthenticationError("User not found")

    # if not user.email_verified_at:
    #     raise AuthenticationError("Email not verified")

    if user.deleted_at:
        raise AuthenticationError("User account is deleted")

    if not bcrypt_context.verify(form_data.password, user.password):
        raise AuthenticationError("Incorrect password")

    token = create_access_token(
        user.email,
        user.id,
        timedelta(minutes=env.get_int("ACCESS_TOKEN_EXPIRE_MINUTES")),
    )
    return Token(access_token=token, token_type="bearer")


def verify_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(
            token, env.get("SECRET_KEY"), algorithms=[env.get("ALGORITHM")]
        )
        user_id: str = payload.get("id")
        return TokenData(user_id=user_id)
    except PyJWTError as e:
        logging.warning(f"Token verification failed: {str(e)}")
        raise AuthenticationError()


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> TokenData:
    return verify_token(token)


CurrentUser = Annotated[TokenData, Depends(get_current_user)]
