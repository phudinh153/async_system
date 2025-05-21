from fastapi import APIRouter, Depends, Request, status
from src.domain.food_item import FoodItemRepository
from src.infrastructure.database.session import get_session_factory
from src.infrastructure.database.tables import FoodItem
from pydantic import BaseModel
from uuid import UUID
from src.infrastructure.utils import authenticate
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix='/food_items',
    tags=['food_items']
)


class FoodItemResponse(BaseModel):
    id: UUID
    name: str
    price: float
    # Add other fields from your FoodItem model

    # Configure ORM mode to allow converting from SQLAlchemy models
    class Config:
        model_config = {"from_attributes": True}


async def get_food_item_repo():
    return FoodItemRepository(get_session_factory())

@router.get('/')
async def read_food_items(request: Request,
                          token: Annotated[str, Depends(oauth_scheme)],
                          repo: FoodItemRepository = Depends(get_food_item_repo)) -> list[FoodItemResponse]:
    """
    Get all food items
    """
    food_items = []
    async for item in repo.get_all():
        food_items.append(item)
    
    return food_items


@authenticate
@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_food_item(request: Request,
                           repo: FoodItemRepository = Depends(get_food_item_repo)) -> FoodItemResponse:
    """
    Create a new food item
    """
    food_item = await request.json()
    food_item = FoodItem(**food_item)
    await repo.create(food_item)
    return food_item


food_items = [
    {"id": 1, "name": "Pizza", "price": 9.99},
    {"id": 2, "name": "Burger", "price": 5.99},
    {"id": 3, "name": "Pasta", "price": 7.99},
]
