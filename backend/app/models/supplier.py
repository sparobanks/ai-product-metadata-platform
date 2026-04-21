from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class Supplier(Base):
    __tablename__ = 'suppliers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    country = Column(String(100), nullable=True)
    contact_email = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    documents = relationship('Document', back_populates='supplier', cascade='all, delete-orphan')
    products = relationship('Product', back_populates='supplier', cascade='all, delete-orphan')
