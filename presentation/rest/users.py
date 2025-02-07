from fastapi import APIRouter
from pydantic import BaseModel, Field, EmailStr, SecretStr

router = APIRouter(
    prefix = '/users'
)


class User(BaseModel):
    name: str = Field(examples=["Phu"])
    email: EmailStr = Field(examples=["phu153@gmail.com"], frozen=True)
    password: SecretStr = Field()

@router.get('/')
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.post('/')
async def create_users(user: User):
    print(user)
    return user