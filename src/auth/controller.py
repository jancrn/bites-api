from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from auth import service as auth_service
from auth.models import RegisterUserRequest, Token
from database import DbSession

router = APIRouter(prefix="/v1/auth", tags=["auth"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: RegisterUserRequest, db: DbSession):
    return auth_service.signup(user, db)


@router.post("/token", response_model=Token)
async def signin(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: DbSession
):
    return auth_service.signin(form_data, db)
