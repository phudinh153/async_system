import sqlalchemy as sa
from sqlalchemy.orm import (
    declarative_base, 
    Mapped, 
    mapped_column,
    relationship
)
from uuid import UUID

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=sa.func.uuid_generate_v4())
    name: Mapped[str] = mapped_column(sa.String(50), nullable=False)
    email: Mapped[str] = mapped_column(sa.String(50), unique=True, nullable=False)
    
    user_auth: Mapped["UserAuth"] = relationship("UserAuth", back_populates="user", uselist=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email})>"

class UserAuth(Base):
    __tablename__ = "user_auth"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=sa.func.uuid_generate_v4())
    user_id: Mapped[UUID] = mapped_column(sa.ForeignKey("users.id"), nullable=False, index=True)
    password: Mapped[str] = mapped_column(sa.String(128), nullable=False)
    
    user: Mapped["User"] = relationship("User", back_populates="user_auth", uselist=False)
    
    def __repr__(self):
        return f"<UserAuth(id={self.id}, user_id={self.user_id})>"

class FoodItem(Base):
    __tablename__ = "food_items"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=sa.func.uuid_generate_v4())
    name: Mapped[str] = mapped_column(sa.String(50), nullable=False)
    price: Mapped[float] = mapped_column(sa.Float, nullable=False)
    
    def __repr__(self):
        return f"<Food(id={self.id}, name={self.name}, price={self.price})>"

class UserFoodItem(Base):
    __tablename__ = "user_food_items"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=sa.func.uuid_generate_v4())
    user_id: Mapped[UUID] = mapped_column(sa.ForeignKey("users.id"), nullable=False, index=True)
    food_item_id: Mapped[UUID] = mapped_column(sa.ForeignKey("food_items.id"), nullable=False, index=True)
    
    user: Mapped["User"] = relationship("User", back_populates="user_food_items")
    food_item: Mapped["FoodItem"] = relationship("FoodItem", back_populates="user_food_items")
    
    def __repr__(self):
        return f"<UserFoodItem(id={self.id}, user_id={self.user_id}, food_item_id={self.food_item_id})>"