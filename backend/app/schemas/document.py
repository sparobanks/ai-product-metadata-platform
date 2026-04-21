from pydantic import BaseModel
from datetime import datetime


class DocumentRead(BaseModel):
    id: int
    supplier_id: int
    filename: str
    document_type: str
    file_path: str
    upload_date: datetime | None = None
    parse_status: str
    ocr_used: bool
    extracted_text: str | None = None

    class Config:
        from_attributes = True
