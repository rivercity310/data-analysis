import json
from sqlmodel import create_engine, Session, SQLModel
from utils.config import Config


DB_URL = Config.read('app', 'db.url')
engine = create_engine(DB_URL, echo=True)


def conn():
    SQLModel.metadata.create_all(engine)
    

def get_db_session():
    with Session(engine) as session:
        yield session
