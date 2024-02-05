from sqlmodel import SQLModel, Field
from enums.patch_severity import PatchSeverity
from enums.patch_status import PatchStatus


class PatchDetail(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
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
                "status": PatchStatus.DOWNLOAD,
                "severity": PatchSeverity.IMPORTANT,
                "issue": "",
                "cve": "CVE-2024-20677",
                "created_at": "2024/02/05",
                "modified_at": "2024/02/05",
                "ahnlab_created_at": "2024/02/05",
                "ahnlab_modified_at": "2024/02/05"
            }
        }
    