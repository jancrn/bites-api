from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

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


# Base class for declarative models
Base = declarative_base()


# Create all tables in the database
Base.metadata.create_all(bind=engine)
