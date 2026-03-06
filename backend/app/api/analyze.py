from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
import os
from uuid import uuid4
import hashlib
import zipfile
import subprocess

from app.core.database import get_db
from app.models.analysis import Analysis
from app.models.issue import Issue
from app.tasks.analyze_task import process_analysis
from app.schemas.repository import RepositoryScan


router = APIRouter(prefix="/analyze", tags=["Analysis"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def compute_file_hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


# --------------------------------
# Scan single C/C++ file
# --------------------------------
@router.post("/")
async def upload_and_analyze(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    if not file.filename.endswith((".c", ".cpp")):
        raise HTTPException(status_code=400, detail="Only .c and .cpp files allowed")

    content = await file.read()

    file_hash = compute_file_hash(content)

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

    unique_name = f"{uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(file_path, "wb") as buffer:
        buffer.write(content)

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

    process_analysis.delay(analysis_record.id, file_path)

    return {
        "analysis_id": analysis_record.id,
        "status": "processing"
    }


# --------------------------------
# Scan ZIP project
# --------------------------------
@router.post("/project")
async def analyze_project(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only ZIP files allowed")

    content = await file.read()

    unique_name = f"{uuid4()}_{file.filename}"
    zip_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(zip_path, "wb") as buffer:
        buffer.write(content)

    extract_dir = os.path.join(UPLOAD_DIR, str(uuid4()))
    os.makedirs(extract_dir, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    analysis_record = Analysis(
        filename=file.filename,
        stored_as=extract_dir,
        score=0,
        status="processing"
    )

    db.add(analysis_record)
    db.commit()
    db.refresh(analysis_record)

    process_analysis.delay(analysis_record.id, extract_dir)

    return {
        "analysis_id": analysis_record.id,
        "status": "processing"
    }


# --------------------------------
# Scan GitHub repository
# --------------------------------
@router.post("/repository")
def analyze_repository(
    repo: RepositoryScan,
    db: Session = Depends(get_db)
):

    repo_url = repo.repo_url

    repo_folder = os.path.join(UPLOAD_DIR, str(uuid4()))

    subprocess.run(
        ["git", "clone", "--depth", "1", repo_url, repo_folder],
        check=True
    )

    analysis_record = Analysis(
        filename=repo_url,
        stored_as=repo_folder,
        score=0,
        status="processing"
    )

    db.add(analysis_record)
    db.commit()
    db.refresh(analysis_record)

    process_analysis.delay(analysis_record.id, repo_folder)

    return {
        "analysis_id": analysis_record.id,
        "status": "processing"
    }


# --------------------------------
# Get analysis result
# --------------------------------
@router.get("/{analysis_id}")
def get_analysis(
    analysis_id: int,
    db: Session = Depends(get_db)
):

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
        "issue_count": len(analysis.issues),
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


# --------------------------------
# Platform statistics
# --------------------------------
@router.get("/stats/summary")
def get_platform_stats(
    db: Session = Depends(get_db)
):

    total_scans = db.query(Analysis).count()

    completed_scans = (
        db.query(Analysis)
        .filter(Analysis.status == "completed")
        .count()
    )

    failed_scans = (
        db.query(Analysis)
        .filter(Analysis.status == "failed")
        .count()
    )

    processing_scans = (
        db.query(Analysis)
        .filter(Analysis.status == "processing")
        .count()
    )

    scores = (
        db.query(Analysis.score)
        .filter(Analysis.status == "completed")
        .all()
    )

    avg_score = 0

    if scores:
        score_values = [s[0] for s in scores]
        avg_score = sum(score_values) / len(score_values)

    total_issues = db.query(Issue).count()

    return {
        "total_scans": total_scans,
        "completed_scans": completed_scans,
        "failed_scans": failed_scans,
        "processing_scans": processing_scans,
        "average_score": round(avg_score, 2),
        "total_issues": total_issues
    }