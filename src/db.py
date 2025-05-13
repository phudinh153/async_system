import sqlalchemy as sa
from sqlalchemy.orm import (
    sessionmaker, 
    declarative_base, 
    Mapped, 
    mapped_column,
    relationship
)

db = sa.create_engine("sqlite:///:memory:")
Session = sessionmaker(db)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(50), nullable=False)
    email: Mapped[str] = mapped_column(sa.String(50), unique=True, nullable=False)
    
    user_auth: Mapped["UserAuth"] = relationship("UserAuth", back_populates="user", uselist=False)
    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email})>"

class UserAuth(Base):
    __tablename__ = "user_auth"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"), nullable=False, index=True)
    password: Mapped[str] = mapped_column(sa.String(128), nullable=False)
    
    user: Mapped["User"] = relationship("User", back_populates="user_auth", uselist=False)
    
    def __repr__(self):
        return f"<UserAuth(id={self.id}, user_id={self.user_id})>"


def main():
    Base.metadata.create_all(db)
    user = User(id=1, name="John Doe", email="p@gmail.com")
    
    with Session.begin() as session:
        session.add(user)
        user_auth = UserAuth(user_id=user.id, password="hashed_password")
        session.add(user_auth)
        session.commit()

    with Session.begin() as session:
        user = session.query(User).filter_by(email="p@gmail.com").first()
        if user:
            print(f"User found: {user}")
            print(f"User Auth: {user.user_auth}")
        else:
            print("User not found.")

if __name__ == "__main__":
    print("Starting the application...")
    main()