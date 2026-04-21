from sqlalchemy.orm import Session

from app.models import Product
from app.services.search.hybrid_search import HybridSearchService


class ProductChatService:
    def __init__(self) -> None:
        self.search_service = HybridSearchService()

    def answer(self, db: Session, query: str, top_k: int = 3) -> dict:
        hits = self.search_service.search(db, query, top_k=top_k)
        products = []
        for hit in hits:
            product = db.query(Product).filter(Product.id == hit.product_id).first()
            if not product:
                continue
            products.append({
                'product_id': product.id,
                'product_name': product.product_name,
                'supplier_name': product.supplier.name if product.supplier else 'Unknown supplier',
                'category': product.category,
                'score': round(hit.score, 4),
                'snippet': hit.chunk_text,
                'attributes': [{
                    'name': a.attribute_name,
                    'value': a.attribute_value,
                    'unit': a.unit,
                } for a in product.attributes],
            })

        summary = 'Top matching products were selected using hybrid semantic search over metadata and extracted document chunks.' if products else 'No matching products were found.'
        return {'summary': summary, 'results': products}
