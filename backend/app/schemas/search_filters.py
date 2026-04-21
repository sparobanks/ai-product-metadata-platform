from pydantic import BaseModel


class HybridSearchRequest(BaseModel):
    query: str
    top_k: int = 5
    category: str | None = None
    supplier_name: str | None = None
    certification: str | None = None
