from pydantic import BaseModel, EmailStr, Field


class TokenParsedUser(BaseModel):
    id: str | None = None
    username: str = Field(..., description="The username of the user")
    email: EmailStr = Field(..., description="The email address of the user")
    full_name: str | None = Field(default=None, description="The full name of the user")
    disabled: bool | None = Field(default=None, description="Indicates if the user is disabled")