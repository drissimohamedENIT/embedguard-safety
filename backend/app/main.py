from fastapi import FastAPI
from app.api.analyze import router as analyze_router

app = FastAPI(title="EmbedGuard Safety API")

app.include_router(analyze_router)

@app.get("/")
def health_check():
    return {"status": "running"}