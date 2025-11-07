from sqlmodel import SQLModel, create_engine, Session
import os
import dotenv

dotenv.load_dotenv()

# SQLite database file
DATABASE_URL = os.getenv("DATABASE_URL")

# create engine
engine = create_engine(DATABASE_URL, echo=True)

# sessions factory
def get_session():
    with Session(engine) as session:
        yield session

# function to create the tables
def init_db():
    SQLModel.metadata.create_all(engine)
