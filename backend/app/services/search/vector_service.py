from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import Product


@dataclass
class RankedProduct:
    product_id: int
    score: float
    snippet: str


class VectorSearchService:
    _model = None

    def __init__(self) -> None:
        if VectorSearchService._model is None:
            VectorSearchService._model = SentenceTransformer(settings.embedding_model)
        self.model = VectorSearchService._model

    def search(self, db: Session, query: str, top_k: int = 5) -> list[RankedProduct]:
        products = db.query(Product).all()
        ranked = self.rank_products(query, products, top_k=top_k)
        return [
            RankedProduct(
                product_id=product.id,
                score=float(score),
                snippet=product.description or self._product_text(product)[:220],
            )
            for product, score in ranked
        ]

    def rank_products(self, query: str, products: list[Product], top_k: int = 5) -> list[tuple[Product, float]]:
        if not products:
            return []
        corpus = [self._product_text(p) for p in products]
        embeddings = self.model.encode(corpus, normalize_embeddings=True)
        query_embedding = self.model.encode([query], normalize_embeddings=True)[0]
        scores = np.dot(embeddings, query_embedding)
        ranked_indices = np.argsort(scores)[::-1][:top_k]
        return [(products[i], float(scores[i])) for i in ranked_indices]

    def _product_text(self, product: Product) -> str:
        attrs = ' '.join(f'{a.attribute_name} {a.attribute_value or ""}' for a in product.attributes)
        certs = ' '.join(c.certification_name or '' for c in getattr(product, 'certifications', []))
        chunks = ' '.join(chunk.chunk_text[:180] for chunk in getattr(product, 'chunks', [])[:2])
        return ' '.join(filter(None, [product.product_name, product.category, product.description, attrs, certs, chunks]))
