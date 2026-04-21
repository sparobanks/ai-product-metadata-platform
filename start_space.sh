#!/usr/bin/env bash
set -e
cd /workspace/backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
cd /workspace/frontend
streamlit run streamlit_app.py --server.port 7860 --server.address 0.0.0.0
