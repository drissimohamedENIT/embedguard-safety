from fastapi import FastAPI

app = FastAPI(title="EmbedGuard Safety API")

@app.get("/")
def health_check():
    return {"status": "running"}