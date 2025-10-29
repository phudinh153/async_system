from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    SecretStr,
    field_validator,
    model_validator,
    ConfigDict,
)
from typing import Dict, Any

class FoodItem(BaseModel):
    model_config = {
        "extra": "forbid",
    }
    name: str = Field(examples=["Pizza"])
    description: str | None = Field(default=None, examples=["Delicious cheese pizza"])
    price: float = Field(gt=0, examples=[9.99])
    category: str = Field(examples=["Italian", "Fast Food", "Vegetarian"])
    nutrients: Dict[str, Dict[str, float]] | None = Field(
        default=None,
        description="Nutrient information in grams",
        examples=[{
            "protein": {"amount": 12.5},
            "carbohydrates": {"amount": 45.2},
            "fat": {"amount": 8.3},
            "fiber": {"amount": 2.1},
            "vitamins": {
                "vitamin_a": 0.003,
                "vitamin_c": 0.012,
                "vitamin_d": 0.0002
            }
        }]
    )

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
    nutrients: Dict[str, Dict[str, float]] | None = None