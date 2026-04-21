from __future__ import annotations


class RAGGenerator:
    def generate(self, query: str, evidence: list[dict]) -> dict:
        if not evidence:
            return {
                'summary': 'No matching evidence was found.',
                'answer': 'I could not find grounded evidence for that query in the uploaded supplier documents.',
            }

        bullets = []
        for item in evidence[:5]:
            bullets.append(
                f"{item['product_name']} from {item['supplier_name']} matched with score {item['score']}. Evidence: {item['chunk_text'][:180]}"
            )
        return {
            'summary': 'Grounded answer generated from retrieved document chunks.',
            'answer': ' '.join(bullets),
        }
