from sqlmodel import SQLModel, create_engine


# SQLite database file
DATABASE_URL = "sqlite:///./yapper.db"

# create engine
engine = create_engine(DATABASE_URL, echo=True)

# function to create the tables
def init_db():
    SQLModel.metadata.create_all(engine)
