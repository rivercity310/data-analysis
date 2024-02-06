from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from sqlalchemy import select
from models.patch import Patch
from database.connection import get_session
from auth.authenticate import authenticate


patch_router = APIRouter(tags=["patch_router"])


@patch_router.get("/")
async def get_all_patches(
    session: Session = Depends(get_session)
) -> list[Patch]:
    stat = select(Patch)
    patches = session.exec(stat).all()
    return patches


@patch_router.get("/{id}")
async def get_patch(
    id: int, 
    session: Session = Depends(get_session)
) -> Patch:
    patch = session.get(Patch, id)
    
    if not patch:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"CAN'T FIND PATCH ENTITY ID {id}"
        )
        
    return patch
    

@patch_router.post("/")
async def add_patch(
    patch: Patch, 
    user: str = Depends(authenticate),
    session: Session = Depends(get_session)
) -> Patch:
    patch.register_user_email = user
    session.add(patch)
    session.commit()
    session.refresh(patch)
    
    return patch
    