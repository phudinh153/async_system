import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from dataclasses import dataclass
from src.infrastructure.database.session import Base
from src.infrastructure.database.tables.food_item import FoodItem


@dataclass
class User(Base):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(
        primary_key=True, default=sa.func.uuid_generate_v4()
    )
    name: Mapped[str] = mapped_column(sa.String(50), nullable=False)
    email: Mapped[str] = mapped_column(sa.String(50), unique=True, nullable=False)

    user_auth: Mapped["UserAuth"] = relationship(
        "UserAuth", back_populates="user", uselist=False
    )
    food_items: Mapped["FoodItem"] = relationship(
        "FoodItem", back_populates="users", secondary="user_food_item"
    )


class UserAuth(Base):
    __tablename__ = "user_auth"
    id: Mapped[UUID] = mapped_column(
        primary_key=True, default=sa.func.uuid_generate_v4()
    )
    user_id: Mapped[UUID] = mapped_column(
        sa.ForeignKey("users.id"), nullable=False, index=True
    )
    password: Mapped[str] = mapped_column(sa.String(128), nullable=False)

    user: Mapped["User"] = relationship(
        "User", back_populates="user_auth", uselist=False
    )

    def __repr__(self):
        return f"<UserAuth(id={self.id}, user_id={self.user_id})>"
