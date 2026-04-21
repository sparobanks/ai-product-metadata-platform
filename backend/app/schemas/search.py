from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


class SearchResult(BaseModel):
    product_id: int
    product_name: str
    supplier_name: str
    score: float
    snippet: str
