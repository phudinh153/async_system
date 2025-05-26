from fastapi import Depends, HTTPException, status
from pydantic import (
    BaseModel,
)
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import timedelta, datetime, timezone
from functools import wraps


def authenticate(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        print("Succeed authentication")
        value = await func(*args, **kwargs)
        return value

    return wrapper


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


class UserMock(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None


class UserInDB(UserMock):
    hashed_password: str


def fake_hash_password(pw):
    return pw + "123"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "50f4672f90876b33026ced17eec19b5c3cb62435100e5b09a3d867c3e349d624"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(fake_db, username: str, password: str):
    fake_db = fake_db or fake_users_db
    user = fake_db.get(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return UserInDB(**user)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)
    if expires_delta:
        expire += expires_delta
    else:
        expire += timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


oauth_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


async def get_current_user(token: str = Depends(oauth_scheme)):
    """
    Dummy function to simulate user retrieval from a token.
    In a real application, you would decode the token and retrieve the user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    if token_data.username is None:
        raise HTTPException(status_code=401, detail="Invalid username in token")
    user = fake_users_db.get(token_data.username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return UserInDB(**user)