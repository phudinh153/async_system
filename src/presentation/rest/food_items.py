from fastapi import APIRouter, Depends, Request, status

router = APIRouter(
    prefix='/food_items',
    tags=['food_items']
)

@router.get('/')
async def read_food_items(request: Request):
    """
    Get all food items
    """
    # Simulate a database call
    food_items = [
        {"id": 1, "name": "Pizza", "price": 9.99},
        {"id": 2, "name": "Burger", "price": 5.99},
        {"id": 3, "name": "Pasta", "price": 7.99}
    ]
    
    return food_items

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_food_item(request: Request):
    """
    Create a new food item
    """
    food_item = await request.json()
    
    # Simulate saving to a database
    food_item["id"] = 4