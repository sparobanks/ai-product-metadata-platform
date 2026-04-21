import re


CERT_PATTERNS = [r'FSC', r'EPD', r'BREEAM', r'LEED', r'ISO\s?14001']
COMPLIANCE_PATTERNS = [r'fire rating', r'class\s?[A-F]', r'CE marked', r'EN\s?\d+', r'BS\s?\d+']
CATEGORY_KEYWORDS = {
    'wall panel': 'Wall Panel',
    'ceiling tile': 'Ceiling Tile',
    'flooring': 'Flooring',
    'door': 'Door',
    'insulation': 'Insulation',
}
ATTRIBUTE_PATTERNS = {
    'dimensions': r'(\d{2,5}\s?[x×]\s?\d{2,5}(?:\s?[x×]\s?\d{1,4})?\s?mm)',
    'thickness': r'thickness[:\s]+(\d+(?:\.\d+)?)\s?(mm|cm|m)?',
    'material': r'material[:\s]+([A-Za-z0-9\-,/ ]+)',
    'warranty': r'warranty[:\s]+(\d+)\s?(years?|months?)',
    'lead_time': r'lead time[:\s]+([A-Za-z0-9 \-]+)',
    'fire_rating': r'(fire rating[:\s]+[A-Za-z0-9\- ]+)',
    'acoustic_rating': r'(NRC\s?\d+(?:\.\d+)?)',
}


class MetadataExtractor:
    def extract(self, text: str, supplier_name: str, document_name: str) -> dict:
        lower = text.lower()
        category = self._infer_category(lower)
        product_name = self._infer_product_name(text, document_name)
        attributes = self._extract_attributes(text)
        certifications = self._extract_certifications(text)
        compliance = self._extract_compliance(text)
        description = self._build_description(text)
        confidence = min(0.95, 0.35 + (0.1 * len(attributes)) + (0.05 * len(certifications)))
        return {
            'product_name': product_name,
            'category': category,
            'brand': supplier_name,
            'description': description,
            'attributes': attributes,
            'certifications': certifications,
            'compliance': compliance,
            'confidence_score': round(confidence, 2),
        }

    def _infer_category(self, lower_text: str) -> str | None:
        for keyword, label in CATEGORY_KEYWORDS.items():
            if keyword in lower_text:
                return label
        return 'General Building Product'

    def _infer_product_name(self, text: str, document_name: str) -> str:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        for line in lines[:8]:
            if 4 < len(line) < 90 and not line.lower().startswith(('page', 'product data sheet', 'technical data')):
                return line
        return document_name.rsplit('.', 1)[0].replace('_', ' ').title()

    def _extract_attributes(self, text: str) -> list[dict]:
        attributes = []
        for name, pattern in ATTRIBUTE_PATTERNS.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if len(match.groups()) > 1:
                    value = match.group(1)
                    unit = match.group(2) if len(match.groups()) >= 2 else None
                else:
                    value = match.group(1)
                    unit = None
                attributes.append({
                    'attribute_name': name,
                    'attribute_value': value.strip(),
                    'unit': unit.strip() if isinstance(unit, str) else unit,
                    'source_snippet': self._snippet(text, match.start(), match.end()),
                    'confidence_score': 0.8,
                })
        return attributes

    def _extract_certifications(self, text: str) -> list[dict]:
        found = []
        for pattern in CERT_PATTERNS:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                found.append({
                    'certification_name': match.group(0).upper(),
                    'certification_code': None,
                    'issuing_body': None,
                    'expiry_date': None,
                })
        unique = []
        seen = set()
        for item in found:
            key = item['certification_name']
            if key not in seen:
                seen.add(key)
                unique.append(item)
        return unique

    def _extract_compliance(self, text: str) -> list[dict]:
        results = []
        for pattern in COMPLIANCE_PATTERNS:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                results.append({
                    'compliance_type': match.group(0),
                    'status': 'mentioned',
                    'notes': self._snippet(text, match.start(), match.end()),
                })
        return results

    def _snippet(self, text: str, start: int, end: int, window: int = 90) -> str:
        return text[max(0, start - window): min(len(text), end + window)].replace('\n', ' ').strip()

    def _build_description(self, text: str, max_len: int = 350) -> str:
        compact = ' '.join(text.split())
        return compact[:max_len] + ('...' if len(compact) > max_len else '')
