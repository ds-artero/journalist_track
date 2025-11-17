from fastapi import FastAPI
from app.routes import search

app = FastAPI(
    title="Universal Web Search Scraper",
    description="API that searches websites, finds results, and returns URLs and titles.",
    version="1.0.0"
)

app.include_router(search.router)

@app.get("/")
def home():
    return {"message": "Welcome to the Web Search Scraper API"}

