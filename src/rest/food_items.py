from fastapi import APIRouter, Depends, Request, status
from src.domain.food_item import FoodItemRepository
from src.infrastructure.database.session import db
from src.infrastructure.database.tables import FoodItem

router = APIRouter(
    prefix='/food_items',
    tags=['food_items']
)

FIRepo = FoodItemRepository(db)

@router.get('/')
async def read_food_items(request: Request):
    """
    Get all food items
    """
    food_items = await FIRepo.get_all()
    
    return food_items

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_food_item(request: Request):
    """
    Create a new food item
    """
    food_item = await request.json()
    food_item = FoodItem(**food_item)
    await FIRepo.create(food_item)
    return food_item


food_items = [
    {"id": 1, "name": "Pizza", "price": 9.99},
    {"id": 2, "name": "Burger", "price": 5.99},
    {"id": 3, "name": "Pasta", "price": 7.99},
]
