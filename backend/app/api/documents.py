from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Document, Supplier
from app.schemas.document import DocumentRead
from app.services.tasks.document_tasks import DocumentTaskService
from app.utils.file_utils import save_upload

router = APIRouter(prefix='/documents', tags=['documents'])
task_service = DocumentTaskService()


@router.post('/upload', response_model=DocumentRead)
def upload_document(
    supplier_name: str = Form(...),
    document_type: str = Form('spec_sheet'),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    supplier = db.query(Supplier).filter(Supplier.name == supplier_name).first()
    if not supplier:
        supplier = Supplier(name=supplier_name)
        db.add(supplier)
        db.commit()
        db.refresh(supplier)

    file_path = save_upload(file, supplier_name)
    document = Document(
        supplier_id=supplier.id,
        filename=file.filename,
        document_type=document_type,
        file_path=file_path,
        parse_status='uploaded',
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


@router.get('', response_model=list[DocumentRead])
def list_documents(db: Session = Depends(get_db)):
    return db.query(Document).order_by(Document.id.desc()).all()


@router.post('/{document_id}/process')
def process_document(document_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail='Document not found')
    return task_service.process_document(db, document_id)
