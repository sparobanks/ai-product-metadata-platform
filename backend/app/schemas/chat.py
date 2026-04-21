from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str
    top_k: int = 5
    category: str | None = None
    certification: str | None = None


class ChatEvidence(BaseModel):
    product_id: int | None = None
    document_id: int
    score: float
    chunk_text: str


class ChatResponse(BaseModel):
    summary: str
    answer: str
    evidence: list[ChatEvidence]
