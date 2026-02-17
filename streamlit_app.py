import streamlit as st
import tempfile
import os

from app.parser import extract_text_from_pdf
from app.processor import clean_text
from app.section_parser import extract_sections
from app.embedder import Embedder
from app.ranker_explainable import rank_resumes_explainable

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="AI Resume Ranker",
    layout="wide"
)

st.title("📄 AI Resume Ranker")
st.subheader("Semantic Resume Screening & Ranking System")

st.markdown(
    """
Upload multiple resumes and provide a job description.  
The system ranks candidates using **transformer-based semantic similarity** and explains *why* each resume ranks where it does.
"""
)

# ------------------ INPUT SECTION ------------------
st.header("🔹 Input")

job_description = st.text_area(
    "Job Description",
    height=200,
    placeholder="Paste the job description here..."
)

uploaded_files = st.file_uploader(
    "Upload Resume PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

# ------------------ PROCESS BUTTON ------------------
if st.button("🚀 Rank Candidates"):

    if not job_description or not uploaded_files:
        st.warning("Please upload resumes and enter a job description.")
        st.stop()

    with st.spinner("Processing resumes..."):

        embedder = Embedder()
        job_embedding = embedder.embed_text(clean_text(job_description))

        resume_sections_map = {}

        for file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(file.read())
                tmp_path = tmp.name

            raw_text = extract_text_from_pdf(tmp_path)
            cleaned_text = clean_text(raw_text)
            sections = extract_sections(cleaned_text)

            resume_sections_map[file.name] = sections

            os.remove(tmp_path)

        ranked_results = rank_resumes_explainable(
            resume_sections_map,
            embedder,
            job_embedding
        )

    # ------------------ OUTPUT SECTION ------------------
    st.header("🏆 Ranked Candidates")

    for idx, item in enumerate(ranked_results, start=1):
        with st.expander(f"#{idx} — {item['resume']}"):
            st.markdown(f"**Score:** `{item['score']:.4f}`")
            st.markdown(f"**Best Matching Section:** `{item['best_section']}`")

            st.markdown("**Section-wise Scores:**")
            for sec, sc in item["section_scores"].items():
                st.write(f"- {sec}: {sc:.4f}")
