from enums.patch_platform import PatchPlatform
from sqlmodel import SQLModel, Field


class Product(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    product_name: str = Field(nullable=False)
    product_architecture: PatchPlatform = Field(nullable=False)
    
    class Config:
        json_schema_extra = {
            "example": {
                "product_id": 1,
                "product_name": "Office 365 ProPlus",
                "product_platform": PatchPlatform.x64
            }
        }
        

class ProductUpdate(SQLModel):
    product_name: str
    product_platform: PatchPlatform