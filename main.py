from app.parser import extract_texts_from_folder
from app.processor import clean_text
from app.embedder import Embedder
from app.section_parser import extract_sections
from app.ranker_explainable import rank_resumes_explainable
from app.shortlisting.threshold_shortlisting import apply_shortlisting
from app.export.csv_exporter import export_results_to_csv

import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

folder_path = "data/sample_resumes"
resume_texts = extract_texts_from_folder(folder_path)

resume_sections_map = {}

for name, text in resume_texts.items():
    cleaned = clean_text(text)
    print("Number of lines after cleaning:",
      len(cleaned.split("\n")))
    sections = extract_sections(cleaned)
    resume_sections_map[name] = sections   

job_description = """
Job Title: Data Scientist
The Mission
We are looking for a Data Scientist who lives at the intersection of data, engineering, and product strategy. You won’t just be building models in a vacuum; you’ll be digging into messy datasets to uncover actionable insights and deploying scalable machine learning solutions that directly impact our bottom line.

What You’ll Do
Build & Deploy: Design, develop, and maintain predictive models and ML pipelines (from EDA to production).

Drive Strategy: Translate complex technical findings into "so what?" insights for non-technical stakeholders.

Experiment: Design A/B tests and statistical frameworks to validate product features and business hypotheses.

Optimize: Collaborate with Data Engineering to improve data quality and streamline our modeling infrastructure.

What You Bring
Technical Toolkit: Proficiency in Python (Pandas, Scikit-learn, PyTorch/TensorFlow) and SQL.

Statistical Foundation: A deep understanding of probability, regression, and the difference between correlation and causation.

The "Engineer" Mindset: Experience with cloud platforms (AWS/GCP/Azure) and version control (Git).

Education: Degree in a quantitative field (CS, Math, Stats, Physics) or equivalent hands-on experience.

Bonus Points For:
Experience with LLMs or Generative AI integration.

Knowledge of MLOps tools (MLflow, Kubeflow, or DVC).

A portfolio of personal projects or Kaggle contributions.
"""

embedder = Embedder()
job_embedding = embedder.embed_text(clean_text(job_description))
# print(resume_sections_map)
# ranked = rank_resumes_by_sections(
#     resume_sections_map,
#     embedder,
#     job_embedding
# )

# print("\n===== SECTION-AWARE RANKING =====")
# for i, (name, score) in enumerate(ranked, start=1):
#     print(f"{i}. {name} -> Score: {score:.4f}")

# print(resume_sections_map)
ranked = rank_resumes_explainable(
    resume_sections_map,
    embedder,
    job_embedding,
    job_description
)

results = apply_shortlisting(ranked)
def print_ranked_results(ranked):

    print("\n" + "=" * 70)
    print("📊 RESUME RANKING RESULTS")
    print("=" * 70)

    for i, res in enumerate(ranked, start=1):

        print(f"\nRank #{i}")
        print("-" * 50)

        print(f"Resume        : {res['resume']}")
        print(f"Final Score   : {res['final_score']:.4f}")
        print(f"JD Score      : {res['jd_score']:.4f}")
        print(f"Market Score  : {res['market_score']:.4f}")
        print(f"Best Section  : {res['best_section']}")
        print(f"Decision      : {res['status']}")

        print("\nSection Breakdown:")
        for section, score in res["section_scores"].items():
            print(f"   {section:<15} → {score:.4f}")

    print("\n" + "=" * 70)

export_results_to_csv(results)
