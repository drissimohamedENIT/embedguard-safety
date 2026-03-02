from fastapi import FastAPI
from app.api.analyze import router as analyze_router
from app.core.database import Base, engine
from app.models.analysis import Analysis
from app.models.issue import Issue

# ✅ FORCE table creation immediately
Base.metadata.create_all(bind=engine)

app = FastAPI(title="EmbedGuard Safety API")

app.include_router(analyze_router)

@app.get("/")
def health_check():
    return {"status": "running"}