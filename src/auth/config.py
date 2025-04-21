from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="v1/auth/signin")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
