from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.session import Base


class DocumentChunk(Base):
    __tablename__ = 'document_chunks'

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey('documents.id'), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=True, index=True)
    chunk_index = Column(Integer, nullable=False)
    page_number = Column(Integer, nullable=True)
    heading = Column(String(255), nullable=True)
    chunk_text = Column(Text, nullable=False)
    chunk_type = Column(String(50), nullable=False, default='document')
    confidence_score = Column(Float, nullable=True)

    document = relationship('Document', back_populates='chunks')
    product = relationship('Product', back_populates='chunks')
