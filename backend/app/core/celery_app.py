from celery import Celery

celery = Celery(
    "embedguard",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["app.tasks.analyze_task"],  # <-- IMPORTANT
)

celery.conf.task_track_started = True