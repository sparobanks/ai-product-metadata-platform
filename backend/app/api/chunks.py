from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import DocumentChunk

router = APIRouter(prefix='/chunks', tags=['chunks'])


@router.get('/document/{document_id}')
def list_document_chunks(document_id: int, db: Session = Depends(get_db)):
    chunks = db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).order_by(DocumentChunk.chunk_index.asc()).all()
    return [
        {
            'id': chunk.id,
            'document_id': chunk.document_id,
            'product_id': chunk.product_id,
            'chunk_index': chunk.chunk_index,
            'page_number': chunk.page_number,
            'heading': chunk.heading,
            'chunk_text': chunk.chunk_text,
            'chunk_type': chunk.chunk_type,
            'confidence_score': chunk.confidence_score,
        }
        for chunk in chunks
    ]
