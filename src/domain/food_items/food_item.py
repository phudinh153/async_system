from src.infrastructure.database.tables import(
    FoodItem, 
    UserFoodItem
)
from typing import AsyncGenerator, Optional
import sqlalchemy as sa

class FoodItemRepository:
    def __init__(self, session_factory):
        # Default to AsyncSession if no session factory is provided
        self.session_factory = session_factory

    async def get_all(self) -> AsyncGenerator[FoodItem, None]:
        async with self.session_factory() as session:
            result = await session.execute(sa.select(FoodItem))

            for item in result.scalars():
                yield item

    async def get_by_id(self, id: int) -> Optional[FoodItem]:
        async with self.session_factory() as session:
            result = await session.execute(sa.select(FoodItem).where(FoodItem.id == id))
            return result.scalar_one_or_none()

    async def create(self, food_item: FoodItem) -> FoodItem:
        async with self.session_factory() as session:
            session.add(food_item)
            await session.commit()
            await session.refresh(food_item)  # Get updated IDs and default values
            return food_item
