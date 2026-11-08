## 2. Recommended Technology Stack

| Layer                                       | Technology                                                    | Purpose        |
| Frontend | React + TypeScript + Tailwind CSS | Application dashboard |
| Backend | Python 3.12 + FastAPI | REST APIs and business logic |
| Data Validation | Pydantic v2 | Structured input/output validation |
| PDF Extraction | PyMuPDF | Extract resume content |
| DOCX Extraction | python-docx | Parse and modify Word resumes |
| Embedding Model | BAAI/bge-small-en-v1.5 | Generate dense semantic embeddings |
| Vector Database | Qdrant | Vector storage and hybrid retrieval |
| Lexical Search | Qdrant BM25 | Keyword-based retrieval |
| Hybrid Fusion | Reciprocal Rank Fusion (RRF) | Combine dense and BM25 results |
| Reranking Model | BAAI/bge-reranker-base | Improve candidate relevance |
| Keyword Matching | Python + RapidFuzz | Exact, alias, and fuzzy matching |
| JD Understanding | LLM + Pydantic | Structured requirement extraction |
| LLM | Gemini / OpenAI | Reasoning, recommendations, cover letters |
| Metadata Database | SQLite + SQLAlchemy | Store metadata, job history, scores |
| Background Processing | Python ingestion worker | Resume indexing |
| Deployment | Docker Compose | Local development and deployment |

### Scoring Architecture

**Engine A — Semantic Relevance**

| Component | Weight |
|---|---:|
| Semantic similarity | 30% |
| Cross-encoder relevance | 30% |
| Responsibility alignment | 20% |
| Project and experience evidence | 20% |

**Engine B — ATS Keyword Matching**

| Component | Weight |
|---|---:|
| Must-have keyword coverage | 45% |
| Technology/tool coverage | 25% |
| Preferred keyword coverage | 10% |
| Role/domain terminology | 10% |
| Keyword evidence and section placement | 10% |

**Final Ranking Formula**

```text
Final Score = (0.55 × Semantic Score)
            + (0.45 × Keyword Score)
```

These weights are initial configuration values and should be calibrated using manually evaluated JD-resume pairs.

Mandatory requirements are evaluated independently and can flag eligibility concerns regardless of the combined score.
