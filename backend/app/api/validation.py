from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Product, ValidationIssue
from app.schemas.validation import ValidationIssueRead
from app.services.validation.validator import ProductValidator

router = APIRouter(prefix='/validation', tags=['validation'])
validator = ProductValidator()


@router.get('/issues', response_model=list[ValidationIssueRead])
def list_issues(db: Session = Depends(get_db)):
    return db.query(ValidationIssue).order_by(ValidationIssue.id.desc()).all()


@router.post('/run/{product_id}')
def run_validation(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return {'message': 'Product not found'}
    issues = validator.run_for_product(db, product)
    return {'message': 'Validation completed', 'issues_found': len(issues)}
