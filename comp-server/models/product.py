from enums import PatchPlatform
from sqlmodel import SQLModel, Field


class Product(SQLModel, table=True):
    __tablename__ = "product"
    
    product_id: int | None = Field(default=None, primary_key=True)
    product_name: str = Field(nullable=False)
    product_architecture: PatchPlatform = Field(nullable=False)
    register_user_id: int = Field(nullable=False, foreign_key="users.user_id")
    
    class Config:
        json_schema_extra = {
            "example": {
                "product_id": 1,
                "product_name": "Office 365 ProPlus",
                "product_platform": PatchPlatform.x64.value
            }
        }
        

class ProductUpdate(SQLModel):
    product_name: str
    product_platform: PatchPlatform