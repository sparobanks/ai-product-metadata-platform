from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text, String, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), nullable=False)
    filename = Column(String(255), nullable=False)
    document_type = Column(String(100), nullable=False, default='spec_sheet')
    file_path = Column(String(500), nullable=False)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    parse_status = Column(String(50), default='uploaded')
    ocr_used = Column(Boolean, default=False)
    extracted_text = Column(Text, nullable=True)

    supplier = relationship('Supplier', back_populates='documents')
    products = relationship('Product', back_populates='source_document')
    chunks = relationship('DocumentChunk', back_populates='document', cascade='all, delete-orphan')
    jobs = relationship('ProcessingJob', back_populates='document', cascade='all, delete-orphan')
