import json
import os
import re
from typing import Any


class LocalStructuredLLM:
    """Lightweight placeholder for Phase 2.

    If OPENAI_API_KEY is present, you can later replace this stub with a real API call.
    For now it extracts a best-effort JSON payload from text so the full pipeline remains runnable.
    """

    def __init__(self) -> None:
        self.provider = os.getenv('LLM_PROVIDER', 'local-rules')
        self.api_key = os.getenv('OPENAI_API_KEY')

    def extract_product_json(self, text: str) -> dict[str, Any]:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        first_line = next((line for line in lines[:10] if 3 < len(line) < 120), 'Unknown Product')
        compact = ' '.join(text.split())[:400]
        material_match = re.search(r'material[:\s]+([A-Za-z0-9\-,/ ]+)', text, re.IGNORECASE)
        dims_match = re.search(r'(\d{2,5}\s?[x×]\s?\d{2,5}(?:\s?[x×]\s?\d{1,4})?\s?mm)', text, re.IGNORECASE)
        fire_match = re.search(r'(fire rating[:\s]+[A-Za-z0-9\- ]+)', text, re.IGNORECASE)
        certs = []
        for cert in ['FSC', 'EPD', 'BREEAM', 'LEED', 'ISO 14001']:
            if cert.lower().replace(' ', '') in text.lower().replace(' ', ''):
                certs.append({'certification_name': cert})
        attributes = []
        if material_match:
            attributes.append({
                'attribute_name': 'material',
                'attribute_value': material_match.group(1).strip(),
                'confidence_score': 0.78,
                'source_snippet': material_match.group(0)[:220],
            })
        if dims_match:
            attributes.append({
                'attribute_name': 'dimensions',
                'attribute_value': dims_match.group(1).strip(),
                'confidence_score': 0.82,
                'source_snippet': dims_match.group(0),
            })
        if fire_match:
            attributes.append({
                'attribute_name': 'fire_rating',
                'attribute_value': fire_match.group(1).replace('fire rating', '').replace(':', '').strip(),
                'confidence_score': 0.79,
                'source_snippet': fire_match.group(0),
            })
        return {
            'product_name': first_line,
            'category': 'General Building Product',
            'description': compact,
            'confidence_score': 0.76,
            'attributes': attributes,
            'certifications': certs,
            'compliance': [],
        }
