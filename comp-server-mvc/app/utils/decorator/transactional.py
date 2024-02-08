from typing import Callable, Any
from fastapi import Depends
from sqlmodel import Session
from utils.connection import get_db_session


class Transactional:
    def __init__(self, func) -> None:
        self.func = func
    
    
    def __call__(self, session: Session = Depends(get_db_session)) -> Callable:
        async def _transactional(*args, **kwargs) -> Any:
            try:
                result = await self.func(*args, **kwargs)
                await session.commit()
                
            except Exception as e:
                session.rollback()
                raise e
            
            return result
        
        return _transactional