import os
from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery = Celery(
    "embedguard",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.tasks.analyze_task"],
)

celery.conf.task_track_started = True