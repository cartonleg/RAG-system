from fastapi import APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController, ProcessController
import os
import aiofiles
from models import ResponseSignal
import logging
from .schemes.data import ProcessRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.AssetModel import AssetModel
from models.db_schemes import DataChunk, Asset
from models.enums.AssetTypeEnum import AssetTypeEnum


logger = logging.getLogger('uvicorn.error')

data_router=APIRouter(prefix='/data')

@data_router.post('/upload/{project_id}')
async def upload_data(request: Request, project_id:str, file:UploadFile, 
                app_settings:Settings = Depends(get_settings)):
    
    project_model = await ProjectModel.create_instance(db_client= request.app.db_client)

    project = await project_model.get_project_or_create_one(project_id=project_id)

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

    asset_model = await AssetModel.create_instance(db_client= request.app.db_client)

    asset_resource = Asset(asset_project_id=project.id, asset_type=AssetTypeEnum.FILE.value, 
                           asset_name=file_name, asset_size=os.path.getsize(file_path))
    
    asset_record = await asset_model.create_asset(asset=asset_resource)
    
    return JSONResponse(content=(ResponseSignal.UPLOAD_SUCCESS.value,
                                 ("file name = " + str(asset_record.id))))

@data_router.post('/process/{project_id}')
async def process_endpoint(project_id: str, process_request: ProcessRequest, request: Request):
    
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset

    project_model = await ProjectModel.create_instance(db_client= request.app.db_client)

    project = await project_model.get_project_or_create_one(project_id=project_id)

    project_files_ids = []
    if process_request.file_id:
        project_files_ids = [process_request.file_id]
    else:
        asset_model = await AssetModel.create_instance(db_client= request.app.db_client)
        project_files = await asset_model.get_all_project_assets(
            asset_project_id = project.id, 
            asset_type = AssetTypeEnum.FILE.value
        )

        project_files_ids = [file["asset_name"] for file in project_files]

    if len(project_files_ids) == 0:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=(ResponseSignal.NO_FILES_ERROR.value))


    processcontroller = ProcessController(project_id=project_id)

    if do_reset == 1:
            _ = await chunk_model.delete_chunks_by_project_id(project_id=project.id)
            
    no_records = 0
    no_files = 0
    for file_id in project_files_ids:
        file_content = processcontroller.get_file_content(file_id=file_id)
        file_chunks = processcontroller.process_file_content(file_content=file_content, 
                                                            file_id=file_id, 
                                                            chunk_size=chunk_size, 
                                                            overlap_size=overlap_size)
        
        if file_chunks == None or len(file_chunks) == 0:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, 
                                content=ResponseSignal.PROCESSING_FAILED)

        
        file_chunks_records = [
            DataChunk(
                chunk_text= chunk.page_content,
                chunk_metadata= chunk.metadata,
                chunk_order= i+1, 
                chunk_project_id= project.id) 
            for i, chunk in enumerate(file_chunks)
            ]
        

        chunk_model = await ChunkModel.create_instance(db_client=request.app.db_client)

        no_records += await chunk_model.insert_many_chunks(chunks=file_chunks_records)
        no_files += 1

    return JSONResponse(content=(ResponseSignal.PROCESSING_SUCCESS.value, 
                                 ("number of inserted chunks = " + str(no_records)),
                                 ("number of processed files = " + str(no_files))))

