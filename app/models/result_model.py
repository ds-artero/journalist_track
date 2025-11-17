from pydantic import BaseModel
from typing import Optional

class SearchResult(BaseModel):
    title: Optional[str]
    url: Optional[str]
    date: Optional[str]

