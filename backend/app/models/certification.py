from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class Certification(Base):
    __tablename__ = 'certifications'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    certification_name = Column(String(100), nullable=False)
    certification_code = Column(String(100), nullable=True)
    issuing_body = Column(String(100), nullable=True)
    expiry_date = Column(String(100), nullable=True)
    source_document_id = Column(Integer, ForeignKey('documents.id'), nullable=True)

    product = relationship('Product', back_populates='certifications')
