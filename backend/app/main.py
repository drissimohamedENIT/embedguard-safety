from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import analyze

app = FastAPI(
    title="EmbedGuard Safety API",
    version="1.0.0"
)

#--------------------------------
# CORS configuration
#--------------------------------
origins = [
    "http://localhost:3000", # React / Next.js dev server
    "http://127.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#--------------------------------
# API routes
#--------------------------------
app.include_router(analyze.router)

@app.get("/")
def root():
    return {"message": "Welcome to EmbedGuard Safety API"}