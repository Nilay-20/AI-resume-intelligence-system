📄 AI Resume Ranking & Screening System
=======================================

> Transformer-based semantic resume ranking with explainable section-wise scoring.

* * * * *

🚀 Overview
-----------

This project is an **AI-powered resume screening and ranking system** that:

-   Extracts structured text from PDF resumes

-   Parses resumes into logical sections

-   Computes semantic similarity against a job description

-   Provides explainable ranking results

-   Displays results via an interactive Streamlit web interface

The system is modular, interpretable, and designed for future scalability.

* * * * *

🧠 Key Features
---------------

-   ✅ Layout-aware PDF extraction using PyMuPDF

-   ✅ Section-based resume parsing

-   ✅ Transformer-based semantic embeddings

-   ✅ Cosine similarity ranking

-   ✅ Explainable scoring (best matching section)

-   ✅ Interactive Streamlit UI

-   ✅ Deterministic and reproducible results

* * * * *

🏗️ System Architecture
-----------------------

`Resume PDFs
     ↓
PyMuPDF Extraction
     ↓
Text Cleaning
     ↓
Section Parsing
     ↓
Embedding Generation (Sentence Transformers)
     ↓
Cosine Similarity Scoring
     ↓
Explainable Ranking
     ↓
Streamlit UI`

* * * * *

📦 Tech Stack
-------------

| Layer | Technology |
| --- | --- |
| PDF Parsing | PyMuPDF (fitz) |
| NLP Embeddings | Sentence Transformers (`all-MiniLM-L6-v2`) |
| Similarity | scikit-learn (Cosine Similarity) |
| Backend Logic | Python |
| UI | Streamlit |

* * * * *

📂 Project Structure
--------------------

`.
├── app/
│   ├── parser_fitz.py
│   ├── processor.py
│   ├── section_parser.py
│   ├── embedder.py
│   ├── ranker_explainable.py
│   └── sections.py
│
├── streamlit_app.py
├── requirements.txt
└── README.md`

* * * * *

⚙️ Installation
---------------

### 1️⃣ Clone the repository

`git clone <your-repo-url>
cd <repo-folder>`

### 2️⃣ Create virtual environment (recommended)

`python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows`

### 3️⃣ Install dependencies

`pip install -r requirements.txt`

* * * * *

▶️ Running the Application
--------------------------

`streamlit run streamlit_app.py`

The app will open automatically in your browser.

* * * * *

📊 How It Works
---------------

### Step 1 --- Upload Resumes

Upload multiple PDF resumes via the Streamlit UI.

### Step 2 --- Enter Job Description

Paste the job description into the input field.

### Step 3 --- Processing Pipeline

-   Extract text using PyMuPDF

-   Clean and normalize text

-   Parse resume into structured sections

-   Generate embeddings for JD and resume sections

-   Compute cosine similarity

### Step 4 --- Ranking & Explainability

Each resume:

-   Receives a semantic similarity score

-   Displays the **best matching section**

-   Shows section-wise similarity breakdown

* * * * *

🧩 Section-Based Scoring Logic
------------------------------

For each resume:

1.  Embed the job description

2.  Embed each parsed section

3.  Compute cosine similarity

4.  Select the highest scoring section

5.  Rank resumes by score

This ensures:

-   Interpretability

-   Section-aware evaluation

-   Transparent AI decisions

* * * * *

📌 Example Output
-----------------

`1. data-scientist-resume-sample.pdf
   Score: 0.7573
   Best Section: Experience

2. candidate_02.pdf
   Score: 0.5985
   Best Section: Skills`

* * * * *

🎯 Design Principles
--------------------

### Modularity

Each component (extraction, parsing, embedding, ranking) is isolated and replaceable.

### Explainability

System returns:

-   Overall similarity score

-   Best contributing section

-   Section-wise breakdown

### Deterministic Behavior

Same input → same ranking results.

### Scalability-Ready

Future-ready for:

-   FastAPI backend

-   FAISS vector indexing

-   AWS deployment

-   Batch resume processing

* * * * *

⚠️ Limitations
--------------

-   Heavily designed resumes may affect section detection

-   No weighted section scoring yet

-   Currently single-machine execution

-   No persistent database storage

* * * * *

🚀 Future Enhancements
----------------------

-   Section-weighted ranking (Experience > Skills)

-   Score threshold-based shortlisting

-   CSV export of ranked results

-   Vector database integration (FAISS)

-   Cloud deployment (AWS EC2)

-   Recruiter authentication layer

-   Market trend integration (RAG)

* * * * *

🧪 Requirements
---------------

Example `requirements.txt`:

`streamlit
pymupdf
sentence-transformers
scikit-learn
numpy`

* * * * *

📈 Why This Project Matters
---------------------------

Traditional keyword-based ATS systems often fail to capture semantic relevance.

This system:

-   Uses transformer embeddings for contextual matching

-   Preserves resume structure for interpretability

-   Provides transparent, section-level explainability

-   Demonstrates applied NLP + system engineering

* * * * *

👨‍💻 Author
------------

Built as an end-to-end AI engineering project demonstrating:

-   NLP modeling

-   Document processing

-   Semantic similarity

-   Explainable AI

-   Interactive UI deployment