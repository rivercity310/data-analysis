from enum import Enum


class PatchStatus(Enum):
    WAIT = 0
    DOWNLOAD = 1
    ZIP = 2
    SIG = 3
    DONE = 4