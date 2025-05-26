from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from src.infrastructure.utils import (
    authenticate_user, get_current_user,
    create_access_token, Token, UserInDB,
)
from src.domain.users import (
    User,
    UserResponse
)

router = APIRouter(
    prefix = '/users'
)


@router.get('/')
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.post('/')
async def create_users(user: User):
    print(user)
    return user

@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """
    Dummy function to simulate user authentication.
    In a real application, you would verify the token and retrieve the user.
    """
    user = authenticate_user(None, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username}
    )

    return Token(access_token=access_token, token_type="bearer")

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(user: Annotated[UserInDB, Depends(get_current_user)]):
    return user
