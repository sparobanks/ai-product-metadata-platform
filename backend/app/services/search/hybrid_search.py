from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session, joinedload

from app.models import Certification, DocumentChunk, Product
from app.services.search.vector_service import VectorSearchService


@dataclass
class HybridSearchResult:
    product_id: int
    product_name: str
    supplier_name: str
    score: float
    chunk_text: str
    document_id: int | None


class HybridSearchService:
    def __init__(self) -> None:
        self.vector_service = VectorSearchService()

    def search(self, db: Session, query: str, top_k: int = 5, category: str | None = None, supplier_name: str | None = None, certification: str | None = None) -> list[HybridSearchResult]:
        products = db.query(Product).options(joinedload(Product.supplier), joinedload(Product.chunks), joinedload(Product.certifications)).all()
        if category:
            products = [p for p in products if (p.category or '').lower() == category.lower()]
        if supplier_name:
            products = [p for p in products if p.supplier and supplier_name.lower() in p.supplier.name.lower()]
        if certification:
            products = [p for p in products if any(certification.lower() in (c.certification_name or '').lower() for c in p.certifications)]
        if not products:
            return []

        ranked = self.vector_service.rank_products(query, products, top_k=top_k)
        results = []
        for product, score in ranked:
            chunk = product.chunks[0].chunk_text if product.chunks else (product.description or '')
            results.append(HybridSearchResult(
                product_id=product.id,
                product_name=product.product_name,
                supplier_name=product.supplier.name if product.supplier else 'Unknown supplier',
                score=score,
                chunk_text=chunk[:320],
                document_id=product.source_document_id,
            ))
        return results
