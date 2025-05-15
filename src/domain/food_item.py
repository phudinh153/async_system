from infrastructure.database.tables import(
    FoodItem, 
    UserFoodItem
)

from typing import AsyncGenerator
import sqlalchemy as sa

class FoodItemRepository():
    def __init__(self, db):
        self.db = db

    async def get_all(self) -> AsyncGenerator[FoodItem]:
        async with self.db.session() as session:
            result = await session.execute(
                sa.select(FoodItem)
            )
            return result.scalars().all()

    async def get_by_id(self, id: int) -> AsyncGenerator[FoodItem]:
        async with self.db.session() as session:
            result = await session.execute(
                sa.select(FoodItem).where(FoodItem.id == id)
            )
            return result.scalar_one_or_none()
    
    async def create(self, food_item: FoodItem) -> FoodItem:
        async with self.db.session() as session:
            session.add(food_item)
            await session.commit()
            return food_item