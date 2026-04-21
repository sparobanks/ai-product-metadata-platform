from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.session import Base


class ComplianceRecord(Base):
    __tablename__ = 'compliance_records'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    compliance_type = Column(String(100), nullable=False)
    status = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    source_document_id = Column(Integer, ForeignKey('documents.id'), nullable=True)

    product = relationship('Product', back_populates='compliance_records')
