from sqlmodel import SQLModel, Session, create_engine
from const import DB_CONN_STR, DB_CONN_ARGS


engine = create_engine(DB_CONN_STR, connect_args=DB_CONN_ARGS, echo=True)


def conn():
    SQLModel.metadata.create_all(engine)
    

def get_session():
    with Session(engine) as session:
        yield session