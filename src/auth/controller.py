from fastapi import APIRouter

from auth import service as auth_service
from auth.exceptions import AuthenticationError
from auth.models import CreateUserRequest
from auth.service import CurrentUser, IsAuthenticated
from database import DbSession
from user.models import User

router = APIRouter(
    prefix="/v1/auth",
)


@router.get(
    "/",
    response_model=User,
)
async def get_user(
    user: CurrentUser,
):
    return {"message": f"Hello, {user.email}! Your user ID is {user.id}"}


@router.post(
    "/",
    response_model=User,
    status_code=201,
)
async def create_user(
    user: CreateUserRequest,
    db: DbSession,
    is_authenticated: IsAuthenticated,
) -> User:
    if not is_authenticated:
        raise AuthenticationError("User is not authenticated")
    return await auth_service.create_user(user, db)
