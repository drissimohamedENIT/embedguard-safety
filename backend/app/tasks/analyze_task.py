from app.core.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.analysis import Analysis
from app.models.issue import Issue
from app.services.analyzer import run_cppcheck
from app.parsers.cppcheck_parser import parse_cppcheck_output
from app.services.classifier import classify_issue
from app.scoring.score_engine import calculate_safety_score

import logging

logger = logging.getLogger(__name__)


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
    time_limit=60
)
def process_analysis(self, analysis_id: int, file_path: str):

    db = SessionLocal()

    try:
        logger.info(f"Starting analysis {analysis_id}")

        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()

        if not analysis:
            logger.error(f"Analysis {analysis_id} not found")
            return

        # Run cppcheck
        raw_output = run_cppcheck(file_path)

        # Parse issues
        parsed_issues = parse_cppcheck_output(raw_output)

        classified_issues = [
            classify_issue(issue) for issue in parsed_issues
        ]

        # Score
        score_data = calculate_safety_score(classified_issues)

        # Save issues
        for issue in classified_issues:
            issue_record = Issue(
                analysis_id=analysis_id,
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

        # Update analysis
        analysis.score = score_data["score"]
        analysis.status = "completed"

        db.commit()

        logger.info(f"Analysis {analysis_id} completed")

    except Exception as e:

        logger.error(f"Analysis {analysis_id} failed: {str(e)}")

        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()

        if analysis:
            analysis.status = "failed"
            db.commit()

        raise self.retry(exc=e)

    finally:
        db.close()