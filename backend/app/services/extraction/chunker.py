from __future__ import annotations


class TextChunker:
    def __init__(self, chunk_size: int = 650, overlap: int = 80) -> None:
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(self, text: str) -> list[dict]:
        cleaned = ' '.join(text.split())
        if not cleaned:
            return []
        chunks = []
        start = 0
        idx = 0
        while start < len(cleaned):
            end = min(len(cleaned), start + self.chunk_size)
            chunk = cleaned[start:end].strip()
            if chunk:
                chunks.append({
                    'chunk_index': idx,
                    'page_number': None,
                    'heading': None,
                    'chunk_text': chunk,
                    'chunk_type': 'document',
                    'confidence_score': 0.7,
                })
                idx += 1
            if end == len(cleaned):
                break
            start = max(0, end - self.overlap)
        return chunks
