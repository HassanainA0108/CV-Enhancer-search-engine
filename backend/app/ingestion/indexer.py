from uuid import uuid5, NAMESPACE_URL
from app.retrieval.hybrid_search import upsert_documents, remove_resume, PROFILE_COLLECTION, CHUNK_COLLECTION
from app.ingestion.section_chunker import make_chunks


def index_resume(resume_id: str, text: str, sections: dict[str,str], profile: dict):
    # Clear stale records on modifications. A failed index run is surfaced to caller.
    remove_resume(resume_id)
    profile_text = (profile.get('summary','') + '\n' + ' '.join(profile.get('skills',[])) + '\n' + text[:7000])[:9000]
    upsert_documents(PROFILE_COLLECTION,[{'id':str(uuid5(NAMESPACE_URL, resume_id + ':profile')), 'resume_id':resume_id, 'section':'profile','text':profile_text,'skills':profile.get('skills',[])}])
    chunks = make_chunks(sections)
    records = [{'id':str(uuid5(NAMESPACE_URL, resume_id + ':chunk:' + str(i))), 'resume_id':resume_id, 'section':c['section'], 'text':c['text']} for i,c in enumerate(chunks)]
    upsert_documents(CHUNK_COLLECTION,records)
    return len(records)
