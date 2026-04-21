from sqlalchemy import Column, Integer, String, Text

from app.db.session import Base


class EmbeddingIndex(Base):
    __tablename__ = 'embeddings_index'

    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(Integer, nullable=False, index=True)
    chunk_text = Column(Text, nullable=False)
