from __future__ import annotations

from sqlalchemy.orm import Session

from app.models import Certification, ComplianceRecord, Document, DocumentChunk, ProcessingJob, Product, ProductAttribute
from app.services.extraction.chunker import TextChunker
from app.services.extraction.llm_extractor import LLMExtractor
from app.services.extraction.metadata_extractor import MetadataExtractor
from app.services.ingestion.document_processor import DocumentProcessor
from app.services.validation.validator import ProductValidator


class DocumentTaskService:
    def __init__(self) -> None:
        self.processor = DocumentProcessor()
        self.rule_extractor = MetadataExtractor()
        self.llm_extractor = LLMExtractor()
        self.chunker = TextChunker()
        self.validator = ProductValidator()

    def process_document(self, db: Session, document_id: int) -> dict:
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise ValueError('Document not found')

        job = ProcessingJob(document_id=document_id, status='processing', stage='extraction', message='Starting extraction pipeline')
        db.add(job)
        db.commit()
        db.refresh(job)

        try:
            text, ocr_used = self.processor.extract_text(document.file_path)
            document.extracted_text = text
            document.ocr_used = ocr_used
            document.parse_status = 'processed'
            job.stage = 'metadata'
            job.message = 'Running rule-based and LLM extraction'
            db.commit()

            rule_payload = self.rule_extractor.extract(text, supplier_name=document.supplier.name, document_name=document.filename)
            payload = self.llm_extractor.extract(text, fallback=rule_payload)

            product = Product(
                supplier_id=document.supplier_id,
                product_name=payload['product_name'],
                category=payload.get('category'),
                brand=payload.get('brand'),
                description=payload.get('description'),
                source_document_id=document.id,
                confidence_score=payload.get('confidence_score', 0.0),
            )
            db.add(product)
            db.commit()
            db.refresh(product)

            for attr in payload.get('attributes', []):
                db.add(ProductAttribute(product_id=product.id, **attr))
            for cert in payload.get('certifications', []):
                db.add(Certification(product_id=product.id, source_document_id=document.id, **cert))
            for compliance in payload.get('compliance', []):
                db.add(ComplianceRecord(product_id=product.id, source_document_id=document.id, **compliance))
            db.commit()

            job.stage = 'chunking'
            job.message = 'Creating searchable document chunks'
            db.commit()
            chunks = self.chunker.split(text)
            for chunk in chunks:
                db.add(DocumentChunk(document_id=document.id, product_id=product.id, **chunk))
            db.commit()

            job.stage = 'validation'
            job.message = 'Running validation checks'
            db.commit()
            issues = self.validator.run_for_product(db, product)

            job.status = 'complete'
            job.stage = 'done'
            job.message = f'Completed successfully with {len(chunks)} chunks and {len(issues)} validation issues.'
            db.commit()
            return {
                'message': 'Document processed successfully',
                'document_id': document.id,
                'product_id': product.id,
                'ocr_used': ocr_used,
                'chunks_created': len(chunks),
                'validation_issues': len(issues),
                'extracted_preview': text[:500],
            }
        except Exception as exc:
            job.status = 'failed'
            job.stage = 'error'
            job.message = str(exc)
            document.parse_status = 'failed'
            db.commit()
            raise
