from pydantic import BaseModel


class ProductAttributeRead(BaseModel):
    attribute_name: str
    attribute_value: str | None = None
    unit: str | None = None
    source_snippet: str | None = None
    confidence_score: float | None = None

    class Config:
        from_attributes = True


class ProductRead(BaseModel):
    id: int
    supplier_id: int
    product_name: str
    category: str | None = None
    subcategory: str | None = None
    brand: str | None = None
    description: str | None = None
    source_document_id: int
    confidence_score: float | None = None
    attributes: list[ProductAttributeRead] = []

    class Config:
        from_attributes = True
