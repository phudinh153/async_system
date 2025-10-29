from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa
from uuid import UUID
from src.infrastructure.database.session import Base
from datetime import datetime
from typing import TYPE_CHECKING, List, Dict, Any

try:
    from sqlalchemy.dialects.postgresql import JSONB
    JSON_TYPE = JSONB
    _HAS_JSONB = True
except ImportError:
    JSON_TYPE = sa.JSON  # SQLite fallback
    _HAS_JSONB = False

if TYPE_CHECKING:
    from src.infrastructure.database.tables.user import User


class FoodItem(Base):
    __tablename__ = "food_items"

    nutrients: Mapped[Dict[str, Any]] = mapped_column(
        JSON_TYPE,
        nullable=True,
        default=dict,
        server_default=sa.text("'{}'::jsonb") if _HAS_JSONB else None,
    )
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
