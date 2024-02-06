from enum import Enum


class PatchLanguage(Enum):
    KR = "ko-kr"
    US = "en-us"
    CN = "zh-cn"
    JP = "ja-jp"
    
    
class PatchPlatform(Enum):
    x64 = "x64"
    x86 = "x86"
    arm64 = "arm64"
    
    
class PatchSeverity(Enum):
    LOW = "Low"
    MODERATE = "Moderate"
    IMPORTANT = "Important"
    CRITICAL = "Critical"
    
    
class PatchStatus(Enum):
    WAIT = 0
    DOWNLOAD = 1
    ZIP = 2
    SIG = 3
    DONE = 4
    

class TokenType(Enum):
    BEARER = "Bearer"