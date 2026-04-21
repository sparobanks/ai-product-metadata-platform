from rapidfuzz import fuzz
from sqlalchemy.orm import Session

from app.models import Product, ValidationIssue


REQUIRED_FIELDS = ['product_name', 'category', 'description']


class ProductValidator:
    def run_for_product(self, db: Session, product: Product) -> list[ValidationIssue]:
        db.query(ValidationIssue).filter(ValidationIssue.product_id == product.id).delete()
        issues: list[ValidationIssue] = []

        for field in REQUIRED_FIELDS:
            if not getattr(product, field, None):
                issues.append(ValidationIssue(
                    product_id=product.id,
                    issue_type='missing_field',
                    severity='high',
                    message=f'{field} is missing',
                    resolved=False,
                ))

        attr_names = {a.attribute_name for a in product.attributes}
        for important in ['material', 'fire_rating', 'dimensions']:
            if important not in attr_names:
                issues.append(ValidationIssue(
                    product_id=product.id,
                    issue_type='missing_attribute',
                    severity='medium',
                    message=f'{important} was not detected',
                    resolved=False,
                ))

        similar_products = db.query(Product).filter(Product.id != product.id).all()
        for other in similar_products:
            score = fuzz.ratio(product.product_name.lower(), other.product_name.lower())
            if score > 88:
                issues.append(ValidationIssue(
                    product_id=product.id,
                    issue_type='possible_duplicate',
                    severity='medium',
                    message=f'Possible duplicate of product #{other.id}: {other.product_name}',
                    resolved=False,
                ))

        for issue in issues:
            db.add(issue)
        db.commit()
        for issue in issues:
            db.refresh(issue)
        return issues
