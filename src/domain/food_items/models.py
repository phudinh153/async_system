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
        examples=[
            {
                "protein": {"amount": 12.5},
                "carbohydrates": {"amount": 45.2},
                "fat": {"amount": 8.3},
                "fiber": {"amount": 2.1},
                "vitamins": {"vitamin_a": 0.003, "vitamin_c": 0.012, "vitamin_d": 0.0002},
            }
        ],
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Name cannot be empty")
        return value.strip()

    @field_validator("nutrients")
    @classmethod
    def validate_nutrients(
        cls, value: Dict[str, Dict[str, float]] | None
    ) -> Dict[str, Dict[str, float]] | None:
        """Normalize and validate nutrients structure.

        This enforces that nutrient amounts are numeric and interpreted as grams.
        Example input accepted:
          {"protein": {"amount": 12.5}, "vitamin_c": {"amount": 0.03}}
        """
        if value is None:
            return None

        normalized: dict = {}
        for nutrient, info in value.items():
            if info is None:
                continue
            if not isinstance(info, dict):
                raise ValueError(f"Nutrient info for '{nutrient}' must be a dict")
            if "amount" not in info:
                raise ValueError(f"Nutrient '{nutrient}' must include an 'amount' field (in grams)")
            amt = info.get("amount")
            if amt is None:
                raise ValueError(
                    f"Nutrient '{nutrient}' must include a non-null 'amount' field (in grams)"
                )
            try:
                amt_f = float(amt)
            except Exception:
                raise ValueError(
                    f"Nutrient amount for '{nutrient}' must be a number representing grams"
                )
            if amt_f < 0:
                raise ValueError(f"Nutrient amount for '{nutrient}' cannot be negative")
            # keep only amount as float to keep stored shape small — unit is grams
            normalized[nutrient] = {"amount": amt_f}

        return normalized


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
