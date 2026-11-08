from app.ingestion.section_chunker import split_sections, make_chunks
from app.ingestion.resume_profiler import profile_resume


def test_sectioning():
    text='Professional Summary\nCloud AI engineer\nSkills\nPython, FastAPI, Azure\nExperience\nBuilt RAG pipelines'
    sections=split_sections(text)
    assert 'skills' in sections
    assert 'experience' in sections
    assert 'FastAPI' in sections['skills']
    assert profile_resume(text,sections)['skills']
    assert len(make_chunks(sections)) >= 3
