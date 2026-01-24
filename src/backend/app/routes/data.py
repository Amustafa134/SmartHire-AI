from click import File
from fastapi import FastAPI, APIRouter, Depends, UploadFile
from backend.app.helpers.config import get_settings, Settings
from backend.app.controllers import DataController

import os

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["data_v1"],
)

@data_router.post("/upload/{project_id}")

async def upload_data(project_id: str, file: UploadFile = File(...),
                       app_settings: Settings = Depends(get_settings)):
    
    # validate the file properties

    is_valid = DataController().validate_uploaded_file(file=file)
    
    if not is_valid:
        raise ValueError("Invalid file.")
    
    return {
        "message": "File uploaded successfully",
        "project_id": project_id,
        "filename": file.filename
    }
    