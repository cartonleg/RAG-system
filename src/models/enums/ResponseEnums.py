from enum import Enum

class ResponseSignal(Enum):
    VAL_SUCCESS = "file validated successfully"
    TYPE_NOT_SUPP = "file type not supported"
    SIZE_EXCEED = "file size exceeded(max 40 MB)"
    UPLOAD_FAIL = "file upload failed"
    UPLOAD_SUCCESS = "file uploeded successfully"
    