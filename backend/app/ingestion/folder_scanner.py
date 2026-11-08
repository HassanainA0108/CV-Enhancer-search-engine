from pathlib import Path
import hashlib


def files_in_folder(folder: str):
    root = Path(folder).resolve()
    root.mkdir(parents=True, exist_ok=True)
    return sorted(p for p in root.rglob('*') if p.is_file() and p.suffix.lower() in {'.pdf', '.docx'} and not p.name.startswith('~$'))


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()
