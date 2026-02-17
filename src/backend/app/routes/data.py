from click import File
from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from backend.app.helpers.config import get_settings, Settings
from backend.app.controllers import DataController, ProjectController
from backend.app.controllers.ProcessController import ProcessController
from backend.app.models.enums.ResponseEnum import ResponseSignal
from backend.app.routes.schemes.data import ProcessRequest

import os
import aiofiles
import logging


logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["data_v1"],
)


# ============================================================
# File Upload Endpoint
# ------------------------------------------------------------

@data_router.post("/upload/{project_id}")

async def upload_data(project_id: str, file: UploadFile = File(...),
                       app_settings: Settings = Depends(get_settings)):
    
    # validate the file properties

    # Initialize data controller (handles validation & file utilities)
    data_controller = DataController()

    # Validate uploaded file (type, size, etc.)
    is_valid, result_signal = data_controller.validate_uploaded_file(file=file)
    
    if not is_valid:
        # Return a 400 response if file validation fails
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": "File validation failed",
                "detail": result_signal
            }
        )
    
    # save the file to the project directory
    # Resolve the project directory path
    project_dir_path = ProjectController().get_project_path(
        project_id=project_id
    )
    
    # Generate a unique file path to prevent overwriting existing files
    file_path, file_id = data_controller.generate_unique_filepath(
        orig_file_name=file.filename,
        project_id=project_id
    )

    try:
        # Save the uploaded file asynchronously in chunks
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(
                app_settings.FILE_DEFAULT_CHUNK_SIZE
            ):
                await f.write(chunk)    # async read

    except Exception as e:
        # Log any unexpected errors during file upload
        logger.error(f"Error while uploading file: {e}")

        # Return a 500 response on upload failure
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": ResponseSignal.FILE_UPLOAD_FAILED.value,
                "detail": str(e)
            }
        )

    # Return success response with uploaded file metadata
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": ResponseSignal.FILE_UPLOADED_SUCCESS.value,
            "file_id": file_id,
            "filename": file.filename
        }
    )
    

# ============================================================
# File Process Endpoint
# ------------------------------------------------------------

@data_router.post("/process/{project_id}")
async def process_endpoint(
    project_id: str, process_request: ProcessRequest):
    
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size

    process_controller = ProcessController(project_id=project_id)

    # Step 1: Get file content
    file_content = process_controller.get_file_content(file_id=file_id)

    # Step 2: Process file content into chunks
    file_chunks = process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        overlap_size=overlap_size
    )

    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": ResponseSignal.PROCESSING_FAILED.value,
                "detail": "File processing failed or resulted in no chunks."
            }
        )
    
    return file_chunks

    # (Further processing like storing chunks can be done here)

    #return JSONResponse(
    #    status_code=status.HTTP_200_OK,
    #    content={
    #        "message": ResponseSignal.PROCESSING_SUCCESS.value,
    #        "file_id": file_id,
    #        "project_id": project_id
    #    }
    #)
