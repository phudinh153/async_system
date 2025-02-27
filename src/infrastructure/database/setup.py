import sqlalchemy as sa

engine = sa.create_engine("sqlite:///:memory:")
connection = engine.connect()

metadata = sa.MetaData()

user_table = sa.Table(
    "user",
    metadata,
    sa.Column("email", sa.String, primary_key=True),
    sa.Column("name", sa.String),
)

def create_user(email, name):
    query = user_table.insert().values(email, name)
    connection.execute(query)

def select_user(email):
    query = user_table.select().where(user_table.c.email == email)
    result = connection.execute(query)
    return result.fetchone()

def main():
    metadata.create_all(engine)
    create_user("p@gmail.com", "phu")
    print(select_user("p@gmail.com"))
    connection.close()

if __name__ == "__main__":
    main()