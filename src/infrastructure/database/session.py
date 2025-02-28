import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column
from dataclasses import dataclass

db = sa.create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=db)
Base = declarative_base()

@dataclass()
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str]
    email: Mapped[str]

def main():
    Base.metadata.create_all(db)
    user = User(username="phu", email="p@gmail.com")
    
    with Session() as session:
        session.add(user)
        session.commit()
        print(session.query(User).all())

if __name__ == "__main__":
    main()