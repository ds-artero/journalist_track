from fastapi import APIRouter, Query
from app.services.scraper import scrape_site

router = APIRouter()

@router.get("/search")
async def search(url: str = Query(..., description="Base website URL"),
                 query: str = Query(..., description="Search term")):
    """
    Example:
    /search?url=https://elpais.com&query=economía
    """
    results = await scrape_site(url, query)
    return {"count": len(results), "results": [r.dict() for r in results]}

