from pathlib import Path

import fitz
import pdfplumber
from PIL import Image
import pytesseract


class DocumentProcessor:
    def extract_text(self, file_path: str) -> tuple[str, bool]:
        path = Path(file_path)
        suffix = path.suffix.lower()
        if suffix in {'.png', '.jpg', '.jpeg', '.tiff', '.bmp'}:
            return self._ocr_image(path), True
        if suffix == '.pdf':
            text = self._extract_pdf_text(path)
            if text.strip():
                return text, False
            return self._ocr_pdf(path), True
        raise ValueError(f'Unsupported file type: {suffix}')

    def _extract_pdf_text(self, path: Path) -> str:
        text_parts: list[str] = []
        with fitz.open(path) as doc:
            for page in doc:
                text_parts.append(page.get_text("text"))
        if ''.join(text_parts).strip():
            return '\n'.join(text_parts)
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text_parts.append(page.extract_text() or '')
        return '\n'.join(text_parts)

    def _ocr_pdf(self, path: Path) -> str:
        with fitz.open(path) as doc:
            chunks = []
            for page in doc:
                pix = page.get_pixmap(dpi=200)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                chunks.append(pytesseract.image_to_string(img))
            return '\n'.join(chunks)

    def _ocr_image(self, path: Path) -> str:
        image = Image.open(path)
        return pytesseract.image_to_string(image)
