from pydantic import BaseModel


class ValidationIssueRead(BaseModel):
    id: int
    product_id: int
    issue_type: str
    severity: str
    message: str
    resolved: bool

    class Config:
        from_attributes = True
