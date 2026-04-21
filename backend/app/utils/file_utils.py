from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import settings


def save_upload(upload_file: UploadFile, supplier_name: str) -> str:
    storage_root = Path(settings.storage_dir)
    supplier_dir = storage_root / supplier_name.lower().replace(' ', '_')
    supplier_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid4().hex}_{upload_file.filename}"
    file_path = supplier_dir / filename
    with file_path.open('wb') as f:
        f.write(upload_file.file.read())
    return str(file_path)
