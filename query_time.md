## 4. Query-Time Architecture

### Objective

Given a job description, identify the most suitable resume through independent semantic and keyword scoring, validate eligibility, and provide explainable recommendations.

### Query Workflow

                      ┌──────────────────────┐
                      │ Job Description Text │
                      └───────────┬──────────┘
                                  │
                                  ▼
                      ┌──────────────────────┐
                      │ JD Analyzer          │
                      │                      │
                      │ Required Skills      │
                      │ Preferred Skills     │
                      │ Responsibilities     │
                      │ Experience           │
                      │ Mandatory Criteria   │
                      └───────────┬──────────┘
                                  │
                   ┌──────────────┴──────────────┐
                   ▼                             ▼
         ┌──────────────────────┐    ┌──────────────────────┐
         │ Engine A             │    │ Engine B             │
         │ Semantic Relevance   │    │ ATS Keyword Matching │
         ├──────────────────────┤    ├──────────────────────┤
         │ Dense Retrieval      │    │ Exact Keywords       │
         │ BM25 Retrieval       │    │ Acronym Matching     │
         │ RRF Fusion           │    │ Alias Matching       │
         │ Cross-Encoder        │    │ Mandatory Coverage   │
         │ Evidence Alignment   │    │ Keyword Evidence     │
         └──────────┬───────────┘    └──────────┬───────────┘
                    │                           │
                    ▼                           ▼
             Semantic Score              Keyword Score
                  /100                        /100
                    │                           │
                    └─────────────┬─────────────┘
                                  ▼
                       ┌──────────────────────┐
                       │ Decision Engine      │
                       │                      │
                       │ Weighted Score       │
                       │ Mandatory Validation │
                       │ Resume-Level Ranking │
                       └───────────┬──────────┘
                                   │
                                   ▼
                       ┌──────────────────────┐
                       │ Top 3–5 Resumes      │
                       │                      │
                       │ Scores               │
                       │ Matched Evidence     │
                       │ Missing Requirements │
                       └───────────┬──────────┘
                                   │
                                   ▼
                       ┌──────────────────────┐
                       │ LLM Intelligence     │
                       │                      │
                       │ Selection Reasoning  │
                       │ Gap Analysis         │
                       │ Resume Enhancements  │
                       │ Cover Letter         │
                       └──────────────────────┘

### Query Execution Steps

| Step | Operation | Technology |
|---|---|---|
| 1 | Analyze JD and extract structured requirements | LLM + Pydantic |
| 2 | Generate dense embedding for the JD | BGE Embedding Model |
| 3 | Perform dense similarity retrieval | Qdrant |
| 4 | Perform BM25 lexical retrieval | Qdrant |
| 5 | Combine retrieval results | RRF |
| 6 | Evaluate keyword coverage across all resumes | Python + RapidFuzz |
| 7 | Merge candidate sets and rerank relevant chunks | Cross-Encoder |
| 8 | Calculate independent semantic and keyword scores | Python |
| 9 | Validate mandatory requirements and rank resumes | Decision Engine |
| 10 | Generate explanation, enhancement suggestions, and cover letter | LLM |

### Example Input

```json
{
  "job_description": "We are looking for an AI Security Consultant with AWS, Kubernetes, IAM, Terraform and AI security experience.",
  "top_k": 5
}
```

### Example Response

```json
{
  "job_title": "AI Security Consultant",
  "recommended_resume": {
    "resume_id": "resume_002",
    "filename": "Cloud_AI_Resume.docx",
    "semantic_score": 88,
    "keyword_score": 92,
    "combined_score": 89.8,
    "eligibility_status": "needs_verification"
  },
  "matched_keywords": [
    "Kubernetes",
    "IAM",
    "AI Security"
  ],
  "missing_keywords": [
    "Terraform"
  ],
  "reasoning": [
    "Strong alignment with cloud security responsibilities.",
    "Relevant Kubernetes and identity-management experience.",
    "Better explicit keyword coverage than other resume variants."
  ],
  "recommendations": [
    {
      "type": "modify",
      "section": "Professional Summary",
      "suggestion": "Emphasize existing cloud and AI security experience using terminology from the job description."
    },
    {
      "type": "verify",
      "section": "Technical Skills",
      "suggestion": "Add Terraform only if supported by actual experience."
    }
  ]
}
```

### Query Latency Targets

These are preliminary estimates for 50–200 resumes, a warmed local model, local Qdrant, and hosted LLM APIs.

| Operation | Estimated Latency |
|---|---:|
| JD parsing | 1–4 seconds |
| JD embedding | 30–200 ms |
| Hybrid search | 10–100 ms |
| Keyword scoring | 20–150 ms |
| Cross-encoder reranking | 0.3–2.5 seconds |
| Score aggregation and ranking | 10–100 ms |
| LLM explanation and recommendations | 2–8 seconds |
| Cover-letter generation | 2–6 seconds |

### Target Performance

| Output | Target |
|---|---|
| Initial resume ranking | 2–6 seconds |
| Reasoning and recommendations | 4–10 seconds |
| Complete workflow including cover letter | 6–16 seconds |

These are engineering targets, not guaranteed response times. Hardware, model choice, concurrent requests, and hosted LLM latency will affect actual performance.

### Optimization Strategies

- Precompute resume embeddings during ingestion.
- Store full extracted resume text for fast keyword evaluation.
- Run hybrid retrieval and deterministic keyword scoring concurrently.
- Rerank only a limited candidate pool.
- Cache JD parsing results using content hashes.
- Keep embedding and reranking models loaded in memory.
- Generate reasoning and cover letters only after ranking.
- Stream or progressively return results to the frontend.
- Track retrieval latency, reranking latency, and end-to-end latency separately.

### Core Design Principle

**Resume selection = Semantic Relevance + Explicit Keyword Alignment + Mandatory Eligibility Validation**

The LLM generates explanations and improvements after ranking. It does not arbitrarily assign the final suitability score.

This architecture prioritizes accurate, explainable resume selection and ATS-oriented optimization while keeping the MVP modular, testable, and suitable for local deployment.