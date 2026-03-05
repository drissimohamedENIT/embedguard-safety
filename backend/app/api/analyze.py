from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
import os
import shutil
from uuid import uuid4
import hashlib

from app.core.database import get_db
from app.models.analysis import Analysis
from app.tasks.analyze_task import process_analysis


router = APIRouter(prefix="/analyze", tags=["Analysis"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def compute_file_hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


@router.post("/")
async def upload_and_analyze(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    if not file.filename.endswith((".c", ".cpp")):
        raise HTTPException(status_code=400, detail="Only .c and .cpp files allowed")

    # Read file content
    content = await file.read()

    # Compute hash
    file_hash = compute_file_hash(content)

    # Check if analysis already exists
    existing = (
        db.query(Analysis)
        .filter(
            Analysis.file_hash == file_hash,
            Analysis.status == "completed"
        )
        .first()
    )

    if existing:
        return {
            "analysis_id": existing.id,
            "status": "cached"
        }

    # Save file
    unique_name = f"{uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(file_path, "wb") as buffer:
        buffer.write(content)

    # Create analysis record
    analysis_record = Analysis(
        filename=file.filename,
        stored_as=unique_name,
        score=0,
        status="processing",
        file_hash=file_hash
    )

    db.add(analysis_record)
    db.commit()
    db.refresh(analysis_record)

    # Queue background job
    process_analysis.delay(analysis_record.id, file_path)

    return {
        "analysis_id": analysis_record.id,
        "status": "processing"
    }


@router.get("/{analysis_id}")
def get_analysis(analysis_id: int, db: Session = Depends(get_db)):

    analysis = (
        db.query(Analysis)
        .options(joinedload(Analysis.issues))
        .filter(Analysis.id == analysis_id)
        .first()
    )

    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return {
        "analysis_id": analysis.id,
        "filename": analysis.filename,
        "score": analysis.score,
        "status": analysis.status,
        "created_at": analysis.created_at,
        "issues": [
            {
                "file": issue.file,
                "line": issue.line,
                "column": issue.column,
                "severity": issue.severity,
                "message": issue.message,
                "rule": issue.rule,
                "category": issue.category,
                "criticality": issue.criticality
            }
            for issue in analysis.issues
        ]
    }