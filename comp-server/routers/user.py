from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from auth.jwt_handler import create_access_token
from sqlmodel import select, Session
from models.user import User, UserDelete, TokenResponse
from database.connection import get_session
from auth.hash_password import HashPassword
from auth.authenticate import authenticate
from enums import TokenType


user_router = APIRouter(tags = ["user_router"])
hash_password = HashPassword()


@user_router.post("/signup")
async def sign_up(
    user: User, 
    session: Session = Depends(get_session)
) -> User:
    stat = select(User).where(User.user_email == user.user_email)
    users = session.exec(stat).all()
    
    if users:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = f"USER EMAIL {user.user_email} IS ALREADY EXISTS"   
        )
    
    user.user_password = hash_password.create_hash(user.user_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user


@user_router.post("/signin")
async def sign_in(
    user: OAuth2PasswordRequestForm = Depends(), 
    session: Session = Depends(get_session)
) -> TokenResponse:
    stat = select(User).where(User.user_email == user.username)
    users = session.exec(stat).all()
    
    for usr in users:
        verified = hash_password.verify_hash(user.password, usr.user_password)
        
        if verified:
            access_token = create_access_token(usr.user_email)
            return {
                "access_token": access_token,
                "token_type": TokenType.BEARER.value
            }
        
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = f"CAN'T FIND USER EMAIL {user.username}"
    )


@user_router.get("/")
async def get_all_users(
    user: str = Depends(authenticate),
    session: Session = Depends(get_session)
):
    stat = select(User)
    return {
        "user": user,
        "data": session.exec(stat).all()
    }


@user_router.delete("/")
async def delete_user(
    user: UserDelete,
    session: Session = Depends(get_session)
) -> User:
    stat = select(User).where(User.user_email == user.user_email)
    find_user = session.exec(stat).first()
    
    if not find_user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"CAN'T FIND USER {user.user_email}"
        )
    
    if hash_password.verify_hash(user.user_password, find_user.user_password):
        session.delete(find_user)
        session.commit()
        return find_user
    
    raise HTTPException(
        status_code = status.HTTP_403_FORBIDDEN,
        detail = "UNVALID PASSWORD"
    )
        