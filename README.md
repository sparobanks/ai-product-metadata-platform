---
title: AI Product Metadata Platform
emoji: 📄
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# AI Product Metadata Platform

A practical Phase 2 MVP for an AI-powered supplier product metadata platform inspired by the KTP role at TSK Group. It ingests supplier PDFs/images, extracts text with OCR fallback, structures product metadata, creates searchable chunks, validates quality issues, and supports hybrid search plus a grounded assistant.

## Phase 2 additions
- LLM-style structured extraction layer with fallback merge
- Searchable document chunks stored in the database
- Hybrid search with optional metadata filters
- Grounded RAG-style assistant with evidence output
- Processing job tracking
- Hugging Face Docker Space support
- Redis/Celery-ready dependencies for future async work

## What is included
- FastAPI backend
- PostgreSQL-ready SQLAlchemy models
- PDF/image ingestion with OCR fallback
- Rule-based extraction plus Phase 2 structured extraction
- Validation engine for missing fields and possible duplicates
- Semantic + hybrid search using sentence-transformers
- Streamlit frontend for upload, processing, search, validation, jobs, and chunks
- Docker + docker-compose setup
- Root Dockerfile for Hugging Face Spaces

## Core workflow
1. Upload supplier document
2. Process document into text
3. Extract rule-based metadata
4. Merge with Phase 2 structured extraction
5. Save product, attributes, certifications, and compliance data
6. Create searchable chunks
7. Run validation checks
8. Search semantically or with hybrid filters
9. Query the grounded assistant and inspect evidence

## Project structure
- `backend/` API, DB models, services
- `frontend/` Streamlit app
- `data/` storage directory and sample docs
- `Dockerfile` + `start_space.sh` for Hugging Face Spaces

## Local quick start
### 1) Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scriptsctivate
pip install -r requirements.txt
export DATABASE_URL=sqlite:///./product_metadata.db
export STORAGE_DIR=../data
uvicorn app.main:app --reload
```

### 2) Frontend
Open a new terminal:
```bash
cd frontend
pip install -r ../backend/requirements.txt
export API_BASE_URL=http://localhost:8000
streamlit run streamlit_app.py
```

### 3) Docker option
```bash
docker-compose up --build
```

## Hugging Face Space
This repo is ready for a Docker Space.
- SDK: Docker
- App port: `7860`
- Backend runs internally on `8000`
- Demo database defaults to SQLite in the Space container

## Example API endpoints
- `POST /documents/upload`
- `POST /documents/{id}/process`
- `GET /jobs`
- `GET /chunks/document/{id}`
- `POST /search/semantic`
- `POST /search/hybrid`
- `POST /chat/query`
- `GET /validation/issues`

## Suggested Phase 3 upgrades
- Replace the local structured extraction stub with a real hosted LLM provider
- Move chunk embeddings into `pgvector`
- Add real background workers with Celery and Redis queues
- Add authentication and role-based access
- Add export to BIM-friendly formats or CSV/JSON templates
- Upgrade the frontend to Next.js

## Demo prompts
- acoustic wall panel with FSC certification
- fire-rated timber ceiling tile
- show products with sustainability credentials
- products with fire rating and timber material
