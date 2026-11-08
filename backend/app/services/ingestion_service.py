from uuid import uuid4
from pathlib import Path
from sqlalchemy import select
from app.config import get_settings
from app.db.models import Resume
from app.db.session import session_scope
from app.ingestion.folder_scanner import files_in_folder, file_hash
from app.ingestion.file_parser import parse_file
from app.ingestion.section_chunker import split_sections
from app.ingestion.resume_profiler import profile_resume
from app.ingestion.indexer import index_resume
from app.retrieval.hybrid_search import ensure_collections, remove_resume


def ingest_folder():
    ensure_collections()
    folder = get_settings().resume_directory
    current = {str(p.resolve()):p for p in files_in_folder(folder)}
    indexed, skipped, removed, failed = 0, 0, 0, []
    with session_scope() as db:
        known = {r.path:r for r in db.execute(select(Resume)).scalars().all()}
        for path, original in current.items():
            try:
                digest = file_hash(original)
                existing = known.get(path)
                if existing and existing.file_hash == digest:
                    skipped += 1
                    continue
                text = parse_file(original)
                if len(text.strip()) < 40:
                    raise ValueError('No meaningful extractable text (scanned PDF may require OCR)')
                sections = split_sections(text)
                profile = profile_resume(text,sections)
                resume_id = existing.id if existing else str(uuid4())
                index_resume(resume_id,text,sections,profile)
                if existing:
                    existing.filename = original.name
                    existing.text = text
                    existing.sections = sections
                    existing.profile = profile
                    existing.file_hash = digest
                else:
                    db.add(Resume(id=resume_id,filename=original.name,path=path,file_hash=digest,text=text,sections=sections,profile=profile))
                db.commit()
                indexed += 1
            except Exception as e:
                db.rollback()
                failed.append(f'{original.name}: {type(e).__name__}: {str(e)[:180]}')
        for old_path, row in known.items():
            if old_path not in current:
                try:
                    remove_resume(row.id)
                    db.delete(row)
                    db.commit()
                    removed += 1
                except Exception as e:
                    db.rollback()
                    failed.append(f'Cannot remove {row.filename}: {e}')
    return {'indexed':indexed,'skipped':skipped,'removed':removed,'failed':failed}
