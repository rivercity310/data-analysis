from fastapi import Depends
from repository.user_repository import UserRepository
from model.user import User
from utils.decorator.transactional import Transactional


class UserService:
    def __init__(self, repo: UserRepository = Depends()):
        self.repo = repo
        
        
    @Transactional
    def get_by_id(self, id: int) -> User:
        res = self.repo.get_by_id(id)
        
        if res is None:
            raise Exception(f"CAN'T FIND USER ID {id}")
        
        return res
    
    
    @Transactional
    def get_by(self) -> list[User]:
        return self.repo.get_by()