from fastapi import APIRouter, UploadFile, File
from services.cv_parser import parse_cv

router = APIRouter(prefix="/cv")

@router.post("/upload")
async def upload_cv(file: UploadFile = File(...)):
    contents = await file.read()
    path = f"uploads/{file.filename}"
    with open(path, "wb") as f:
        f.write(contents)

    parsed = parse_cv(path)
    return parsed
