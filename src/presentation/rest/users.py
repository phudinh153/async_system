from fastapi import APIRouter
from pydantic import (
    BaseModel, Field, EmailStr, SecretStr,
    field_validator, field_serializer,
    model_validator
)
import re

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
    @classmethod
    def check_passwords_matched(cls, values):
        if values.password != values.password_repeat:
            return ValueError("Passwords do not match")
        return values
    

@router.get('/')
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.post('/')
async def create_users(user: User):
    print(user)
    return user