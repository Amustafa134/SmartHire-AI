from click import File
from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from backend.app.helpers.config import get_settings, Settings
from backend.app.controllers import DataController, ProjectController
from backend.app.models.enums.ResponseEnum import ResponseSignal

import os
import aiofiles
import logging


logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["data_v1"],
)

@data_router.post("/upload/{project_id}")

async def upload_data(project_id: str, file: UploadFile = File(...),
                       app_settings: Settings = Depends(get_settings)):
    
    # validate the file properties

    data_controller = DataController()

    is_valid, result_signal = data_controller.validate_uploaded_file(file=file)
    
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": "File validation failed",
                "detail": result_signal
            }
        )
    
    # save the file to the project directory
    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path, file_id = data_controller.generate_unique_filepath(
        orig_file_name=file.filename,
        project_id=project_id
    )

    try:
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)    # async read

    except Exception as e:

        logger.error(f"Error while uploading file: {e}")

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": ResponseSignal.FILE_UPLOAD_FAILED.value,
                "detail": str(e)
            }
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": ResponseSignal.FILE_UPLOADED_SUCCESS.value,
            "file_id": file_id,
            "filename": file.filename
        }
    )
    

    