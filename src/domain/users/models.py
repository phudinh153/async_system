import re
from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    SecretStr,
    field_validator,
    model_validator,
)


class Account:
    _name: str
    _password: str

    def __init__(self):
        self._name = "phuxa"
        self._password = "123456"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if len(name) not in range(3, 9):
            raise ValueError("Length of name must be between 3-8 characters!")

        pattern = r"^[a-zA-Z0-9_-]+$"
        if not re.match(pattern, name):
            raise ValueError("Unexpected characters!")

        self._name = name

    def set_password(self, password):
        self._password = password

    # def set_name(self, name):
    #     self._name = name

    # def get_name(self):
    #     return self._name

    def get_password(self):
        return self._password


VALID_NAME_REGEX = re.compile(r"^[a-zA-Z0-9_]{3,20}$")

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


class TokenParsedUser(BaseModel):
    id: str | None = None
    username: str = Field(..., description="The username of the user")
    email: EmailStr = Field(..., description="The email address of the user")
    full_name: str | None = Field(default=None, description="The full name of the user")
    disabled: bool | None = Field(
        default=None, description="Indicates if the user is disabled"
    )


class UserResponse(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None
