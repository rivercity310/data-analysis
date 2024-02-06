from sqlmodel import SQLModel, Field
from pydantic import BaseModel


class User(SQLModel, table=True):
    __tablename__ = "users"
    
    user_id: int | None = Field(default=None, primary_key=True)
    user_email: str = Field(nullable=False, unique=True)
    user_password: str = Field(nullable=False)
    
    
class UserDelete(BaseModel):
    user_email: str
    user_password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str