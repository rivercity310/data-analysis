from fastapi import Depends
from sqlmodel import Session, select
from utils.connection import get_db_session
from model.user import User


class UserRepository:
    def __init__(self, session: Session = Depends(get_db_session)) -> None:
        self.db = session
        
    
    def get_by_id(self, id: int) -> User | None:
        stat = select(User, id)
        return self.db.exec(stat).first()
        
    
    def get_by(self) -> list[User]:
        stat = select(User)
        return self.db.exec(stat).all()