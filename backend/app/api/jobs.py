from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import ProcessingJob

router = APIRouter(prefix='/jobs', tags=['jobs'])


@router.get('')
def list_jobs(db: Session = Depends(get_db)):
    jobs = db.query(ProcessingJob).order_by(ProcessingJob.id.desc()).all()
    return [
        {
            'id': job.id,
            'document_id': job.document_id,
            'status': job.status,
            'stage': job.stage,
            'message': job.message,
            'created_at': job.created_at,
            'updated_at': job.updated_at,
        }
        for job in jobs
    ]
