from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    SecretStr,
    field_validator,
    model_validator,
    ConfigDict,
)

class FoodItem(BaseModel):
    model_config = {
        "extra": "forbid",
    }
    name: str = Field(examples=["Pizza"])
    description: str | None = Field(default=None, examples=["Delicious cheese pizza"])
    price: float = Field(gt=0, examples=[9.99])
    category: str = Field(examples=["Italian", "Fast Food", "Vegetarian"])

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Name cannot be empty")
        return value.strip()

class FoodItemResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
    )

    id: str
    name: str
    description: str | None = None
    price: float
    category: str