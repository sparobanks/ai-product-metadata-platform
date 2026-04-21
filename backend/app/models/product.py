from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), nullable=False)
    product_name = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=True)
    subcategory = Column(String(100), nullable=True)
    brand = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    source_document_id = Column(Integer, ForeignKey('documents.id'), nullable=False)
    confidence_score = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    supplier = relationship('Supplier', back_populates='products')
    source_document = relationship('Document', back_populates='products')
    attributes = relationship('ProductAttribute', back_populates='product', cascade='all, delete-orphan')
    certifications = relationship('Certification', back_populates='product', cascade='all, delete-orphan')
    compliance_records = relationship('ComplianceRecord', back_populates='product', cascade='all, delete-orphan')
    validation_issues = relationship('ValidationIssue', back_populates='product', cascade='all, delete-orphan')
    chunks = relationship('DocumentChunk', back_populates='product', cascade='all, delete-orphan')
