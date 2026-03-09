from app.core.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.analysis import Analysis
from app.utils.file_scanner import discover_source_files
from app.tasks.file_analysis_task import analyze_single_file
from app.tasks.aggregate_analysis_task import finalize_analysis

from celery import chord

import logging

logger = logging.getLogger(__name__)


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
    time_limit=600,
    soft_time_limit=540
)
def process_analysis(self, analysis_id: int, file_path: str):

    db = SessionLocal()

    try:

        logger.info(f"Starting analysis {analysis_id}")

        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()

        if not analysis:
            logger.error(f"Analysis {analysis_id} not found")
            return

        # Discover C/C++ files
        files = discover_source_files(file_path)

        if not files:
            logger.warning("No source files found")

            analysis.status = "completed"
            analysis.score = 100

            db.commit()
            return

        logger.info(f"Discovered {len(files)} source files")

        # Create chord (parallel tasks + aggregation)
        job = chord(
            analyze_single_file.s(f) for f in files
        )

        job(
            finalize_analysis.s(
                analysis_id,
                file_path
            )
        )

    except Exception as e:

        logger.error(f"Analysis {analysis_id} failed: {str(e)}")

        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()

        if analysis:
            analysis.status = "failed"
            db.commit()

        raise self.retry(exc=e)

    finally:
        db.close()