from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController, ProcessController
import os
import aiofiles
from models import ResponseSignal
import logging
from .schemes.data import ProcessRequest


logger = logging.getLogger('uvicorn.error')

data_router=APIRouter(prefix='/data')

@data_router.post('/upload/{project_id}')
async def upload_data(project_id:str, file:UploadFile, 
                app_settings:Settings = Depends(get_settings)):
    is_valid, reason = DataController().val_file(file=file)
    
    if not is_valid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, 
                            content=f'status: {reason}')
    
    proj_path = ProjectController().get_project_path(project_id=project_id)
    file_path, file_name = DataController().gen_unique_filepath(orig_filename=file.filename, 
                                                     project_id=project_id)

    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        
        logger.error(f'File upload error: {e}')

        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, 
                            content=ResponseSignal.UPLOAD_FAIL.value)

    return JSONResponse(content=(ResponseSignal.UPLOAD_SUCCESS.value,
                                 ("file name = " + file_name)))

@data_router.post('/process/{project_id}')
async def process_endpoint(project_id: str, process_request: ProcessRequest):
    
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size

    processcontroller = ProcessController(project_id=project_id)

    file_content = processcontroller.get_file_content(file_id=file_id)
    file_chunks = processcontroller.process_file_content(file_content=file_content, 
                                                         file_id=file_id, 
                                                         chunk_size=chunk_size, 
                                                         overlap_size=overlap_size)
    
    if file_chunks == None or len(file_chunks) == 0:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, 
                            content=ResponseSignal.PROCESSING_FAILED)
    
    return file_chunks
