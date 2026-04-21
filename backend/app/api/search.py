from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Product
from app.schemas.search import SearchRequest
from app.schemas.search_filters import HybridSearchRequest
from app.services.rag.chat_service import ProductChatService
from app.services.search.hybrid_search import HybridSearchService
from app.services.search.vector_service import VectorSearchService

router = APIRouter(prefix='/search', tags=['search'])
vector_service = VectorSearchService()
hybrid_service = HybridSearchService()
chat_service = ProductChatService()


@router.post('/semantic')
def semantic_search(payload: SearchRequest, db: Session = Depends(get_db)):
    hits = vector_service.search(db, payload.query, top_k=payload.top_k)
    results = []
    for hit in hits:
        product = db.query(Product).filter(Product.id == hit.product_id).first()
        if product:
            results.append({
                'product_id': product.id,
                'product_name': product.product_name,
                'supplier_name': product.supplier.name if product.supplier else 'Unknown supplier',
                'score': round(hit.score, 4),
                'snippet': hit.snippet,
            })
    return {'results': results}


@router.post('/hybrid')
def hybrid_search(payload: HybridSearchRequest, db: Session = Depends(get_db)):
    hits = hybrid_service.search(
        db,
        payload.query,
        top_k=payload.top_k,
        category=payload.category,
        supplier_name=payload.supplier_name,
        certification=payload.certification,
    )
    return {
        'results': [
            {
                'product_id': hit.product_id,
                'product_name': hit.product_name,
                'supplier_name': hit.supplier_name,
                'score': round(hit.score, 4),
                'snippet': hit.chunk_text,
                'document_id': hit.document_id,
            }
            for hit in hits
        ]
    }


@router.post('/chat')
def chat_search(payload: SearchRequest, db: Session = Depends(get_db)):
    return chat_service.answer(db, payload.query, top_k=payload.top_k)
