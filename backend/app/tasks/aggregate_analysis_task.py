from app.core.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.analysis import Analysis
from app.models.issue import Issue
from app.scoring.score_engine import calculate_safety_score

import logging
import os
import shutil

logger = logging.getLogger(__name__)


def cleanup_workspace(path: str):
    """
    Remove uploaded file / extracted project / cloned repository
    after analysis completes.
    """

    try:

        if os.path.isfile(path):
            os.remove(path)

        elif os.path.isdir(path):
            shutil.rmtree(path)

    except Exception as e:
        logger.warning(f"Cleanup failed for {path}: {str(e)}")


@celery_app.task
def finalize_analysis(results, analysis_id, workspace_path):

    db = SessionLocal()

    try:

        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()

        if not analysis:
            logger.error(f"Analysis {analysis_id} not found")
            return

        all_issues = []

        # Aggregate issues from all workers
        for file_issues in results:
            if file_issues:
                all_issues.extend(file_issues)

        # Save issues
        for issue in all_issues:

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

        # Calculate score
        score_data = calculate_safety_score(all_issues)

        analysis.score = score_data["score"]
        analysis.status = "completed"

        db.commit()

        logger.info(f"Analysis {analysis_id} completed with {len(all_issues)} issues")

    except Exception as e:

        logger.error(f"Analysis {analysis_id} failed: {str(e)}")

        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()

        if analysis:
            analysis.status = "failed"
            db.commit()

    finally:

        # Clean workspace after analysis
        cleanup_workspace(workspace_path)

        db.close()