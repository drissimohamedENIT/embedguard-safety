from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
from uuid import uuid4
from app.services.analyzer import run_cppcheck

router = APIRouter(prefix="/analyze", tags=["Analysis"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/")
async def upload_and_analyze(file: UploadFile = File(...)):

    if not file.filename.endswith((".c", ".cpp")):
        raise HTTPException(status_code=400, detail="Only .c and .cpp files allowed")

    unique_name = f"{uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    analysis_output = run_cppcheck(file_path)

    return {
        "filename": file.filename,
        "stored_as": unique_name,
        "analysis_raw": analysis_output
    }