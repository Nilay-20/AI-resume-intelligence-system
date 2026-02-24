from app.parser import extract_texts_from_folder
from app.processor import clean_text
from app.section_parser import extract_sections
from app.embedder import Embedder
from app.ranker_explainable import rank_resumes_explainable
from app.shortlisting.threshold_shortlisting import apply_shortlisting
from app.justification.batch_justifier import BatchJustificationGenerator
from app.export.csv_exporter import export_results_to_csv

import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

UPLOAD_DIR = "storage/uploads"


def run_evaluation(job_description: str, progress_callback=None):

    embedder = Embedder()

    # -----------------------------
    # Extract resumes
    # -----------------------------
    if progress_callback:
        progress_callback("parsing", "Parsing resumes")
    resume_texts = extract_texts_from_folder(
        UPLOAD_DIR
    )

    resume_sections_map = {}

    for name, text in resume_texts.items():

        cleaned = clean_text(text)
        sections = extract_sections(cleaned)

        resume_sections_map[name] = sections

    # -----------------------------
    # Embed Job Description
    # -----------------------------
    job_embedding = embedder.embed_text(
        job_description
    )

    # -----------------------------
    # Ranking
    # -----------------------------
    if progress_callback:
        progress_callback("ranking", "Ranking candidates")
    results = rank_resumes_explainable(
        resume_sections_map,
        embedder,
        job_embedding,
        job_description
    )

    # -----------------------------
    # Shortlisting
    # -----------------------------
    results = apply_shortlisting(results)

    # -----------------------------
    # Justification
    # -----------------------------
    if progress_callback:
        progress_callback("justification", "Generating AI justifications")
    justifier = BatchJustificationGenerator()

    justifications = justifier.generate(
        results,
        job_description,
        resume_sections_map
    )

    just_map = {
        j["resume"]: j["justification"]
        for j in justifications
    }

    for res in results:
        res["justification"] = just_map.get(
            res["resume"], ""
        )

    # -----------------------------
    # CSV Export
    # -----------------------------
    if progress_callback:
        progress_callback("exporting", "Preparing final report")
    csv_path = export_results_to_csv(results)

    return {
        "results": results,
        "csv_path": csv_path
    }