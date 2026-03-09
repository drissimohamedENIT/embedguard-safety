from app.core.celery_app import celery_app
from app.services.analyzer import run_cppcheck
from app.parsers.cppcheck_parser import parse_cppcheck_output
from app.services.classifier import classify_issue


@celery_app.task
def analyze_single_file(file_path: str):

    raw_output = run_cppcheck(file_path)

    parsed = parse_cppcheck_output(raw_output)

    classified = [
        classify_issue(issue) for issue in parsed
    ]

    return classified