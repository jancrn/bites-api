from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import env
from auth.controller import router as auth_router
from database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    init_db()


app = FastAPI(
    title=env.get("APP_NAME"),
    description=env.get("APP_DESCRIPTION"),
    version=env.get("APP_VERSION"),
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    auth_router,
    prefix="/v1/api",
    tags=["auth"],
)
