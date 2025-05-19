from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa
from uuid import UUID
from src.infrastructure.database.session import Base
from datetime import datetime
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from src.infrastructure.database.tables.user import User


class FoodItem(Base):
    __tablename__ = "food_items"

    name: Mapped[str] = mapped_column(sa.String(50), nullable=False)
    price: Mapped[float] = mapped_column(sa.Float, nullable=False)
    users: Mapped[List["User"]] = relationship(
        "User", back_populates="food_items", secondary="user_food_item"
    )

    def __repr__(self):
        return f"<Food(id={self.id}, name={self.name}, price={self.price})>"


class UserFoodItem(Base):
    __tablename__ = "user_food_item"
    __table_args__ = (
        sa.UniqueConstraint("user_id", "food_item_id", name="uq_user_food_item"),
        {"extend_existing": True}
    )

    # Remove inherited primary key
    id = None

    # Define composite primary key
    user_id: Mapped[UUID] = mapped_column(
        sa.ForeignKey("users.id", 
                    #   ondelete="CASCADE"
                      ),
        primary_key=True
    )
    food_item_id: Mapped[UUID] = mapped_column(
        sa.ForeignKey("food_items.id", 
                    #   ondelete="CASCADE"
                      ),
        primary_key=True
    )

    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime, default=sa.func.now(), nullable=False
    )

    def __repr__(self):
        return (
            f"<UserFoodItem(user_id={self.user_id}, food_item_id={self.food_item_id})>"
        )
