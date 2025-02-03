from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseSignal

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale = 1048576 # MB to bytes

    def val_file(self, file):
        try:
            if file.content_type not in self.app_settings.ALLOWED_FILE_TYPE:
                return False, ResponseSignal.TYPE_NOT_SUPP.value
            if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
                return False, ResponseSignal.SIZE_EXCEED.value
            return True, ResponseSignal.VAL_SUCCESS.value
        except Exception as e:
            return False, ResponseSignal.UPLOAD_FAIL.value
