from __future__ import annotations

from sqlalchemy.orm import Session

from app.services.search.hybrid_search import HybridSearchService


class RAGRetriever:
    def __init__(self) -> None:
        self.search_service = HybridSearchService()

    def retrieve(self, db: Session, query: str, top_k: int = 5, **filters) -> list[dict]:
        hits = self.search_service.search(db, query, top_k=top_k, **filters)
        return [
            {
                'product_id': hit.product_id,
                'document_id': hit.document_id,
                'score': round(hit.score, 4),
                'chunk_text': hit.chunk_text,
                'product_name': hit.product_name,
                'supplier_name': hit.supplier_name,
            }
            for hit in hits
        ]
