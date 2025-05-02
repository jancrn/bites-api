from sqlmodel import select

from database import DbSession
from user.models import User


def get_user_by_email(
    db: DbSession,
    email: str,
) -> User | None:
    return db.execute(select(User).where(User.email == email)).scalars().first()


def get_user_by_id(
    db: DbSession,
    user_id: str,
) -> User | None:
    return db.execute(select(User).where(User.id == user_id)).scalars().first()
