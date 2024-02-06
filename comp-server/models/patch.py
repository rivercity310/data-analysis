from sqlmodel import SQLModel, Field
from enums import PatchLanguage
from enums import PatchStatus


class Patch(SQLModel, table=True):
    __tablename__ = "patch"
    
    id: int | None = Field(default=None, primary_key=True)
    patch_title: str = Field(nullable=False)
    patch_summary: str = Field(nullable=False)
    patch_language: PatchLanguage = Field(nullable=False)
    patch_status: PatchStatus = Field(nullable=False)
    register_user_email: str = Field(nullable=False)
    patch_detail_id: int | None = Field(nullable=False, foreign_key="patch_detail.patch_detail_id")
    product_id: int | None = Field(nullable=False, foreign_key="product.product_id")
    
    
    class Config:
        json_schema_extra = {
            "example": {
                "patch_title": "Microsoft Office 365 (인터넷 연결이 필요한 패치입니다)",
                "patch_summary": "이 업데이트는 CVE-2024-20677의 Microsoft Office 보안 취약성을 해결합니다.",
                "patch_language": PatchLanguage.KR.value,
                "patch_detail_id": 1,
                "product_id": 1
            }
        }