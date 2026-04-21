from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.chat import ChatRequest
from app.services.rag.generator import RAGGenerator
from app.services.rag.retriever import RAGRetriever

router = APIRouter(prefix='/chat', tags=['chat'])
retriever = RAGRetriever()
generator = RAGGenerator()


@router.post('/query')
def chat_query(payload: ChatRequest, db: Session = Depends(get_db)):
    evidence = retriever.retrieve(
        db,
        payload.query,
        top_k=payload.top_k,
        category=payload.category,
        certification=payload.certification,
    )
    response = generator.generate(payload.query, evidence)
    return {**response, 'evidence': evidence}
