from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseSignal
import re
import os

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
        
    def gen_unique_filename(self, orig_filename: str, project_id: str):
        rand_key = self.random_string_generator()
        project_path = ProjectController().get_project_path(project_id=project_id)
        file_name = self.clean_filename(orig_filename=orig_filename)

        file_path = os.path.join(project_path, rand_key + '_' + file_name)

        while os.path.exists(file_path):
            rand_key = self.random_string_generator()
            file_path = os.path.join(project_path, rand_key + '_' + file_name)
        
        return file_path

    def clean_filename(self, orig_filename:str):
        output = (re.sub(r'[^\w.]', '', orig_filename.strip())).replace(' ', '_')
        return output

