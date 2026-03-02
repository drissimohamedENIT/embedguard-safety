from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
from uuid import uuid4
from app.services.analyzer import run_cppcheck
from app.parsers.cppcheck_parser import parse_cppcheck_output
from app.services.classifier import classify_issue
from app.scoring.score_engine import calculate_safety_score
from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.database import get_db
from app.models.analysis import Analysis
from app.models.issue import Issue
from sqlalchemy.orm import joinedload

router = APIRouter(prefix="/analyze", tags=["Analysis"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)



@router.post("/")
async def upload_and_analyze(
    file: UploadFile = File(...),    
    db: Session = Depends(get_db)
):

    if not file.filename.endswith((".c", ".cpp")):
        raise HTTPException(status_code=400, detail="Only .c and .cpp files allowed")

    unique_name = f"{uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run static analysis
    analysis_output = run_cppcheck(file_path)

    # Parse raw output
    parsed_issues = parse_cppcheck_output(analysis_output)

    # Apply safety classification
    classified_issues = [
        classify_issue(issue) for issue in parsed_issues
    ]

    score_data = calculate_safety_score(classified_issues)

    # Save analysis
    analysis_record = Analysis(
        filename=file.filename,
        stored_as=unique_name,
        score=score_data["score"]
    )
    db.add(analysis_record)
    db.commit()
    db.refresh(analysis_record)

    for issue in classified_issues:
        issue_record = Issue(
            analysis_id=analysis_record.id,
            file=issue["file"],
            line=issue["line"],
            column=issue["column"],
            severity=issue["severity"],
            message=issue["message"],
            rule=issue["rule"],
            category=issue["category"],
            criticality=issue["criticality"]
        )
        db.add(issue_record)

    db.commit()

    return {
        "analysis_id": analysis_record.id,
        "filename": file.filename,
        "issue_count": len(classified_issues),
        "score": score_data["score"],
        "breakdown": score_data["breakdown"],
        "issues": classified_issues
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