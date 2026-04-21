from __future__ import annotations

from app.core.llm import LocalStructuredLLM
from app.schemas.llm_extraction import LLMExtractionResult


class LLMExtractor:
    def __init__(self) -> None:
        self.client = LocalStructuredLLM()

    def extract(self, text: str, fallback: dict | None = None) -> dict:
        raw = self.client.extract_product_json(text)
        merged = self._merge(fallback or {}, raw)
        result = LLMExtractionResult(**merged)
        return result.model_dump()

    def _merge(self, fallback: dict, llm_data: dict) -> dict:
        merged = dict(fallback)
        for key in ['product_name', 'category', 'brand', 'description', 'confidence_score']:
            if llm_data.get(key):
                merged[key] = llm_data[key]
        merged['attributes'] = self._dedupe_list((fallback.get('attributes') or []) + (llm_data.get('attributes') or []), 'attribute_name')
        merged['certifications'] = self._dedupe_list((fallback.get('certifications') or []) + (llm_data.get('certifications') or []), 'certification_name')
        merged['compliance'] = self._dedupe_list((fallback.get('compliance') or []) + (llm_data.get('compliance') or []), 'compliance_type')
        if 'brand' not in merged:
            merged['brand'] = fallback.get('brand')
        return merged

    def _dedupe_list(self, items: list[dict], key: str) -> list[dict]:
        seen = set()
        output = []
        for item in items:
            value = (item.get(key) or '').strip().lower()
            if not value or value in seen:
                continue
            seen.add(value)
            output.append(item)
        return output
