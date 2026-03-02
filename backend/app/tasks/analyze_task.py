from app.core.celery_app import celery
from app.services.analyzer import run_cppcheck
from app.parsers.cppcheck_parser import parse_cppcheck_output
from app.services.classifier import classify_issue
from app.scoring.score_engine import calculate_safety_score
from app.core.database import SessionLocal
from app.models.analysis import Analysis
from app.models.issue import Issue


@celery.task
def process_analysis(analysis_id: int, file_path: str):

    db = SessionLocal()

    try:
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        if not analysis:
            return

        # Run static analysis
        raw_output = run_cppcheck(file_path)
        parsed = parse_cppcheck_output(raw_output)
        classified = [classify_issue(issue) for issue in parsed]
        score_data = calculate_safety_score(classified)

        # Save issues
        for issue in classified:
            issue_record = Issue(
                analysis_id=analysis.id,
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

        analysis.score = score_data["score"]
        analysis.status = "completed"

        db.commit()

    except Exception:
        analysis.status = "failed"
        db.commit()

    finally:
        db.close()