from datetime import datetime
from typing import List

from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    firebase_uuid: str


class FirebaseToken(BaseModel):
    class FirebaseInfo(BaseModel):
        class FirebaseIdentities(BaseModel):
            email: List[str] = []

        identities: FirebaseIdentities
        sign_in_provider: str

    iss: str
    aud: str
    auth_time: int
    user_id: str
    sub: str
    iat: int
    exp: int
    email: str
    email_verified: bool
    firebase: FirebaseInfo

    def get(self, key: str) -> str | bool:
        return getattr(self, key)

    def is_expired(self) -> bool:
        return datetime.now().timestamp() > self.exp
