FROM python:3.11-slim
WORKDIR /workspace
RUN apt-get update && apt-get install -y --no-install-recommends     build-essential     tesseract-ocr     poppler-utils     curl     && rm -rf /var/lib/apt/lists/*
COPY backend/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY . /workspace
ENV DATABASE_URL=sqlite:///./hf_demo.db
ENV STORAGE_DIR=/workspace/data
ENV API_BASE_URL=http://127.0.0.1:8000
EXPOSE 7860
CMD ["bash", "start_space.sh"]
