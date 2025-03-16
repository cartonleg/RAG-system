from enum import Enum

class ResponseSignal(Enum):
    VAL_SUCCESS = "file validated successfully"
    TYPE_NOT_SUPP = "file type not supported"
    SIZE_EXCEED = "file size exceeded(max 40 MB)"
    UPLOAD_FAIL = "file upload failed"
    UPLOAD_SUCCESS = "file uploeded successfully"
    PROCESSING_FAILED = "file failed to process"
    PROCESSING_SUCCESS = "file processed succesfully"
    NO_FILES_ERROR = "no files found"
    FILE_ID_ERROR = "no file found with this id"
    PROJECT_NOT_FOUND_ERROR = "project not found"
    INSERT_INTO_VECTORDB_ERROR = "error while inserting into vectordb"
    INSERT_INTO_VECTORDB_SUCCESS = "inserted into vectordb succesfully"
    VECTORDB_COLLECTION_RETRIEVED = "vectordb collection info retrieved"
    VECTORDB_SEARCH_ERROR = "error while searching vectordb"
    VECTORDB_SEARCH_SUCCESS = "vectordb searched succesfully"
    