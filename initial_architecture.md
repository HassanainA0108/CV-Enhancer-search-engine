# AI Resume Intelligence & ATS Optimization Platform

## 1. High-Level System Architecture

The proposed application uses a **modular Python FastAPI architecture** with two independent scoring engines: a Semantic Relevance Engine and an ATS Keyword Matching Engine.

### Architecture Diagram


                         ┌──────────────────────┐
                         │    React Frontend    │
                         │                      │
                         │ - Job Description    │
                         │ - Resume Library     │
                         │ - Ranking Dashboard  │
                         │ - Recommendations    │
                         │ - Cover Letter       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   FastAPI Backend    │
                         │                      │
                         │ - API Orchestration  │
                         │ - Data Validation    │
                         │ - Job Management     │
                         └──────────┬───────────┘
                                    │
                   ┌────────────────┴────────────────┐
                   ▼                                 ▼
         ┌────────────────────┐           ┌────────────────────┐
         │ Ingestion Pipeline │           │   Query Pipeline   │
         │                    │           │                    │
         │ - Folder Scanner   │           │ - JD Analyzer      │
         │ - PDF/DOCX Parser  │           │ - Hybrid Retrieval │
         │ - Section Chunking │           │ - Semantic Scoring │
         │ - Embedding        │           │ - Keyword Scoring  │
         │ - Vector Indexing  │           │ - Final Ranking    │
         └─────────┬──────────┘           └─────────┬──────────┘
                   │                                │
                   ▼                                ▼
         ┌────────────────────┐           ┌────────────────────┐
         │ Storage Layer      │           │ LLM Intelligence   │
         │                    │           │                    │
         │ Qdrant             │           │ - Explainability   │
         │ - Dense Vectors    │           │ - Gap Analysis     │
         │ - BM25             │           │ - Resume Changes   │
         │ - Resume Chunks    │           │ - Cover Letter     │
         │                    │           │                    │
         │ SQLite             │           └────────────────────┘
         │ - Metadata         │
         │ - Resume Versions  │
         │ - Job History      │
         └────────────────────┘
```

### Core Components

**Frontend Layer**
- Accept job descriptions in text format.
- Display available resumes.
- Show semantic and keyword scores independently.
- Display ranking and selection reasoning.
- Present resume enhancement recommendations.
- Generate cover-letter content.

**FastAPI Backend**
- Expose REST APIs.
- Coordinate ingestion and query processing.
- Manage job analysis and resume comparison.
- Maintain resume metadata and application history.

**Retrieval and Scoring**
- Dense semantic similarity search.
- BM25 lexical retrieval.
- Reciprocal Rank Fusion (RRF).
- Cross-encoder reranking.
- Independent exact keyword matching.
- Mandatory requirement validation.
- Final resume-level ranking.

**LLM Intelligence**
- Analyze job descriptions.
- Explain why a resume is suitable.
- Identify missing requirements.
- Suggest additions, replacements, and removals.
- Generate tailored cover letters.
