from sqlmodel import SQLModel, Field
from enums import PatchSeverity
from enums import PatchStatus


class PatchDetail(SQLModel, table=True):
    __tablename__ = "patch_detail"
    
    patch_detail_id: int | None = Field(default=None, primary_key=True)
    bulletin_id: str = Field(nullable=False)
    bulletin_url: str = Field(nullable=False)
    patch_status: PatchStatus = Field(nullable=False)
    patch_severity: str = Field(nullable=False)
    issue: str = Field(nullable=False)
    cve: str = Field(nullable=False)
    created_at: str = Field(nullable=False)
    modified_at: str = Field(nullable=False)
    ahnlab_create_at: str = Field(nullable=False)
    ahnlab_modified_at: str = Field(nullable=False)
  
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "bulletin_id": "1234",
                "bulletin_url": "https://learn.microsoft.com/ko-kr/officeupdates/current-channel",
                "status": PatchStatus.DOWNLOAD.value,
                "severity": PatchSeverity.IMPORTANT.value,
                "issue": "",
                "cve": "CVE-2024-20677",
                "created_at": "2024/02/05",
                "modified_at": "2024/02/05",
                "ahnlab_created_at": "2024/02/05",
                "ahnlab_modified_at": "2024/02/05"
            }
        }
    