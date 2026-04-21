from pydantic import BaseModel, Field


class ExtractedAttribute(BaseModel):
    attribute_name: str
    attribute_value: str | None = None
    unit: str | None = None
    source_snippet: str | None = None
    confidence_score: float = 0.75


class ExtractedCertification(BaseModel):
    certification_name: str
    certification_code: str | None = None
    issuing_body: str | None = None
    expiry_date: str | None = None


class ExtractedCompliance(BaseModel):
    compliance_type: str
    status: str | None = None
    notes: str | None = None


class LLMExtractionResult(BaseModel):
    product_name: str
    category: str | None = None
    brand: str | None = None
    description: str | None = None
    confidence_score: float = Field(default=0.75, ge=0.0, le=1.0)
    attributes: list[ExtractedAttribute] = []
    certifications: list[ExtractedCertification] = []
    compliance: list[ExtractedCompliance] = []
