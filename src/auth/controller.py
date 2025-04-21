from fastapi import APIRouter
from starlette import status

from auth import service as auth_service
from auth.models import SignInUserRequest, SignUpUserRequest, Token
from database import DbSession
from user.models import User

router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=User)
async def signup(user: SignUpUserRequest, db: DbSession) -> User:
    return auth_service.signup(user, db)


@router.post("/signin", status_code=status.HTTP_200_OK, response_model=Token)
async def signin(form_data: SignInUserRequest, db: DbSession):
    return auth_service.signin(form_data, db)
