## 3. Ingestion-Time Architecture

### Objective

Process all locally stored resumes, extract their information, create section-aware chunks, generate embeddings, and store searchable data.

Ingestion runs independently of the query pipeline.

### Ingestion Workflow

                   ┌─────────────────────┐
                   │ Local Resume Folder │
                   │                     │
                   │ data/resumes/       │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │ Folder Scanner      │
                   │                     │
                   │ SHA-256 Validation  │
                   │ New/Modified Files  │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │ Document Parser     │
                   │                     │
                   │ PDF / DOCX          │
                   │ Text Extraction     │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │ Resume Structuring  │
                   │                     │
                   │ Summary             │
                   │ Skills              │
                   │ Experience          │
                   │ Projects            │
                   │ Certifications      │
                   │ Education           │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │ Section-Aware       │
                   │ Chunking            │
                   └──────────┬──────────┘
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
       ┌─────────────────┐         ┌─────────────────┐
       │ Dense Embedding │         │ BM25 Indexing   │
       │                 │         │                 │
       │ BGE Model       │         │ Lexical Search  │
       └────────┬────────┘         └────────┬────────┘
                │                           │
                └─────────────┬─────────────┘
                              ▼
                   ┌─────────────────────┐
                   │ Qdrant Database     │
                   │                     │
                   │ resume_profiles     │
                   │ resume_chunks       │
                   └─────────────────────┘

### Ingestion Steps

1. Scan the local resume directory for `.pdf` and `.docx` files.
2. Generate SHA-256 hashes to detect new, modified, or duplicate files.
3. Extract text using the appropriate parser.
4. Identify resume sections such as skills, experience, projects, and certifications.
5. Build structured resume profiles.
6. Create section-aware chunks while preserving their source locations.
7. Generate dense embeddings for profiles and chunks.
8. Index lexical text for BM25 retrieval.
9. Store vectors and payloads in Qdrant.
10. Store original extracted text, file metadata, hashes, and version history in SQLite.

### Qdrant Collections

**Collection A: `resume_profiles`**

Stores one searchable profile representation per resume.

```json
{
  "resume_id": "resume_001",
  "base_resume_id": "base_001",
  "variant_id": "variant_security",
  "filename": "AI_Security_Resume.docx",
  "target_roles": [
    "AI Security Engineer"
  ],
  "skills": [
    "Python",
    "Azure",
    "RAG",
    "AI Governance"
  ],
  "experience_years": 2.5,
  "profile_text": "AI Engineer with experience in...",
  "embedding_model": "BAAI/bge-small-en-v1.5"
}
```

**Collection B: `resume_chunks`**

Stores individual resume sections and supporting evidence.

```json
{
  "resume_id": "resume_001",
  "chunk_id": "resume_001_experience_02",
  "section": "experience",
  "text": "Implemented AI observability...",
  "skills": [
    "OpenTelemetry",
    "AI Monitoring"
  ],
  "source_location": "experience.paragraph_4"
}
```

Each Qdrant point additionally contains indexed vectors, which are separate from the JSON payload shown above.

### Incremental Ingestion

Resume file discovered
        │
        ▼
Calculate SHA-256
        │
        ▼
Compare with stored hash
        │
        ├── Unchanged → Skip indexing
        │
        └── Changed / New
                │
                ▼
         Parse and chunk
                │
                ▼
         Generate embeddings
                │
                ▼
         Upsert new vectors
                │
                ▼
         Remove stale vectors
                │
                ▼
         Update metadata


The ingestion process should use stable document identifiers and safe replacement operations to prevent stale chunks or partially indexed resumes.
