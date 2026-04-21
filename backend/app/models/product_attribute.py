from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.session import Base


class ProductAttribute(Base):
    __tablename__ = 'product_attributes'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    attribute_name = Column(String(100), nullable=False)
    attribute_value = Column(String(255), nullable=True)
    unit = Column(String(50), nullable=True)
    source_snippet = Column(Text, nullable=True)
    confidence_score = Column(Float, default=0.0)

    product = relationship('Product', back_populates='attributes')
