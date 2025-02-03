from .BaseController import BaseController
from fastapi import UploadFile

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale = 1048576 # MB to bytes

    def val_file(self, file):
        try:
            if file.content_type not in self.app_settings.ALLOWED_FILE_TYPE:
                return False, 'file type not supported'
            if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
                return False, 'file size too large'
            return True
        except Exception as e:
            print(f"Validation error: {e}")
            return False