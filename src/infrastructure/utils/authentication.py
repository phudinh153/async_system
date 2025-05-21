from functools import wraps
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from typing import Annotated
from src.domain.users import TokenParsedUser


def authenticate(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        print("Succeed authentication")
        value = await func(*args, **kwargs)
        return value
    
    return wrapper


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def fake_decode_token(token: str):
    return TokenParsedUser(username=token + "_user", email=token + "@example.com")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenParsedUser:
    """
    Dummy function to simulate user authentication.
    In a real application, you would verify the token and retrieve the user.
    """
    # Simulate token verification and user retrieval
    user = fake_decode_token(token)
    return user
