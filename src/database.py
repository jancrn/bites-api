from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlmodel import SQLModel

import env

load_dotenv()


engine = create_engine(env.get("DATABASE_URL"))


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Type alias for the database session
DbSession = Annotated[Session, Depends(get_db)]


def init_db():
    if env.get("DEV_MODE") == "True":
        print("Initializing database...")
        SQLModel.metadata.drop_all(bind=engine)
        SQLModel.metadata.create_all(bind=engine)
