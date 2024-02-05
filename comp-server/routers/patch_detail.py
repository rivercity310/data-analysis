from fastapi import APIRouter, Depends
from sqlmodel import select
from models.patch_detail import PatchDetail
from database.connection import get_session


patch_detail_router = APIRouter(tags=["patch_detail"])


@patch_detail_router.get("/")
async def get_all_patch_detail(session=Depends(get_session)) -> list[PatchDetail]:
    stat = select(PatchDetail)
    return session.exec(stat).all()