from fastapi import APIRouter, Depends, UploadFile
from helpers.config import get_settings, Settings


data_router=APIRouter(prefix='/data')

@data_router.post('/upload/{project_id}')
def upload_data(project_id:str, file:UploadFile, 
                app_settings:Settings = Depends(get_settings)):
    pass