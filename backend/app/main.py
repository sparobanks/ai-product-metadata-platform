from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import documents, products, search, validation
from app.api import chat, jobs, chunks
from app.core.config import settings
from app.db.session import Base, engine
import app.models  # noqa: F401

Path(settings.storage_dir).mkdir(parents=True, exist_ok=True)
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(documents.router)
app.include_router(products.router)
app.include_router(search.router)
app.include_router(validation.router)
app.include_router(chat.router)
app.include_router(jobs.router)
app.include_router(chunks.router)


@app.get('/')
def root():
    return {'message': 'AI Product Metadata Platform API is running'}
