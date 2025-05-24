from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from pydantic import (
    BaseModel, Field, EmailStr, SecretStr,
    field_validator, field_serializer,
    model_validator
)
import re
from src.infrastructure.utils import get_current_user
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix = '/users'
)

VALID_NAME_REGEX = re.compile(r'^[a-zA-Z0-9_]{3,20}$')

class User(BaseModel):
    model_config = {
        "extra": "forbid",
    }
    name: str = Field(examples=["Phu"])
    email: EmailStr = Field(examples=["phu153@gmail.com"], frozen=True)
    password: SecretStr = Field(exclude=True)
    password_repeat: SecretStr = Field(exclude=True)
    
    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str):
        if not VALID_NAME_REGEX.match(v):
            raise ValueError("Invalid name")
        return v
    
    @model_validator(mode="after")
    def check_passwords_matched(self):
        if self.password != self.password_repeat:
            raise ValueError("Passwords do not match")
        return self


@router.get('/')
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.post('/')
async def create_users(user: User):
    print(user)
    return user

@router.get("/me")
async def get_current_user_profile(user: User = Depends(get_current_user)):
    return user

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "secret123",
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

@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Dummy function to simulate user authentication.
    In a real application, you would verify the token and retrieve the user.
    """
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    if not user.hashed_password == fake_hash_password(form_data.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    return {"access_token": user.username, "token_type": "bearer"}
