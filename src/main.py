from fastapi import FastAPI

from auth.controller import router as auth_router

app = FastAPI()

app.include_router(
    auth_router,
    prefix="/v1/api",
    tags=["auth"],
)
