from pathlib import Path
import fitz
from docx import Document


def parse_file(path: Path) -> str:
    if path.suffix.lower() == '.pdf':
        with fitz.open(path) as pdf:
            return '\n'.join(page.get_text(sort=True) for page in pdf).strip()
    if path.suffix.lower() == '.docx':
        doc = Document(str(path))
        lines = [p.text for p in doc.paragraphs if p.text.strip()]
        for table in doc.tables:
            for row in table.rows:
                lines.append(' | '.join(cell.text for cell in row.cells))
        return '\n'.join(lines).strip()
    raise ValueError('Only .pdf and .docx are supported')
