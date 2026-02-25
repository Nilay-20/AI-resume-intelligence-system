# AI Resume Intelligence System

Transformer-based resume screening pipeline with explainable section-level scoring and retrieval-augmented market alignment.

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![SentenceTransformers](https://img.shields.io/badge/SentenceTransformers-all--MiniLM--L6--v2-FF6F00?style=flat-square)](https://sbert.net)


---

## Pipeline

```
Resume PDFs
    │
    ▼
PDF Extraction (PyMuPDF)
    │
    ▼
Section Parser — Experience · Skills · Projects
    │
    ▼
Transformer Embeddings (all-MiniLM-L6-v2)
    │
    ▼
Section-wise Cosine Similarity vs JD Embedding
    │
    ├──── Base JD Alignment Score (0.7×)
    │
    ▼
RAG Market Intelligence Module
  Role Inference → LLM Market Synthesis → Market Embedding
    │
    ├──── Market Alignment Score (0.3×)
    │
    ▼
Weighted Score Aggregation
    │
    ▼
Ranked Output + Explainability Metadata + CSV Report
```

---

## What It Does

- Parses resumes into semantic sections and evaluates each section independently against the job description — not the full document as a blob
- Computes cosine similarity between transformer embeddings of each resume section and the JD, returning the highest-contributing section as the explainability signal
- Infers job role from the JD and runs a RAG pipeline to synthesize real-world market expectations, embedding them into the same vector space for competitiveness scoring
- Final score: `0.7 × JD similarity + 0.3 × market alignment`
- Async evaluation pipeline via FastAPI Background Tasks — non-blocking, job-isolated, supports batch processing
- React dashboard for upload, live progress polling, ranked visualization, and CSV export

---

## Tech Stack

| Layer | Technology |
|---|---|
| PDF Extraction | PyMuPDF |
| Embedding Model | SentenceTransformers `all-MiniLM-L6-v2` |
| Similarity | Cosine Similarity — scikit-learn |
| RAG Pipeline | Role inference + LLM market synthesis |
| Backend | FastAPI + Background Tasks |
| Storage | Job-isolated filesystem |
| Frontend | React + Tailwind CSS |
| Output | REST API + CSV Report |

---

## Project Structure

```
Resume_ranker/
│
├── app/
│   ├── parser.py                   # PDF text extraction
│   ├── processor.py                # Text cleaning and normalization
│   ├── section_parser.py           # Resume section detection
│   ├── embedder.py                 # Transformer embedding interface
│   ├── ranker_explainable.py       # Section scoring and ranked output
│   │
│   ├── market_intelligence/
│       ├── role_detector.py        # JD role inference
│       ├── market_pipeline.py      # RAG orchestration
│       ├── market_generator.py     # LLM market context synthesis
│       └── market_cache.py         # Market embedding cache
│   
├── backend/
│   ├── main.py                     # FastAPI entrypoint
│   ├── routes/                     # Endpoint definitions
│   ├── services/                   # Async evaluation workers
│   └── jobs/                       # Job lifecycle management
│
├── frontend/                       # React dashboard
├── storage/                        # Job-isolated uploads and results
└── requirements.txt
```

---

## Quickstart

```bash
git clone https://github.com/Nilay-20/Resume_ranker.git
cd Resume_ranker

# Backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
uvicorn backend.main:app --reload
# API: http://127.0.0.1:8000

# Frontend
cd frontend
npm install
npm run dev
# UI: http://localhost:5173
```

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/job/create` | Initialize a new evaluation session |
| `POST` | `/files/upload-resumes` | Upload resume PDFs for a job session |
| `POST` | `/evaluation/evaluate` | Start async evaluation pipeline |
| `GET` | `/evaluation/status/{job_id}` | Poll pipeline progress |
| `GET` | `/evaluation/results/{job_id}` | Retrieve ranked candidates |
| `GET` | `/evaluation/download/{job_id}` | Download CSV report |

---

## How the AI Pipeline Works

**Parsing.** Resumes are extracted using layout-aware PDF parsing and segmented into semantic sections — Experience, Skills, Projects. Structured segmentation enables localized comparison rather than evaluating resumes as flat text blobs.

**Section-Level Scoring.** Each section and the job description are independently encoded using a SentenceTransformer model. Cosine similarity is computed per section against the JD embedding. The best-matching section determines the base alignment score and serves as the explainability output — the system reports *why* a candidate ranked where they did.

**RAG Market Augmentation.** The job role is inferred from the JD. A RAG pipeline synthesizes real-world market hiring expectations via LLM inference and embeds the result into the same vector space. Candidates are evaluated against this market embedding, adjusting raw JD alignment scores with a competitiveness signal that reflects actual hiring standards — not just JD keyword overlap.

**Final Ranking.** `Final Score = 0.7 × JD Alignment + 0.3 × Market Alignment`. Candidates are ranked deterministically. Each result includes score, status (Shortlisted / Review / Rejected), and contributing section metadata. Output is served via API and exportable as a CSV report.

---

## Roadmap

- Cross-encoder re-ranking layer for top-K precision improvement
- Fine-tune embedding model on hiring-domain corpora
- Migrate market RAG to persistent retrieval corpus
- Distributed async workers for high-volume batch inference
- Multi-tenant job isolation with authentication
