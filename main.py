from app.parser import extract_texts_from_folder
from app.processor import clean_text
from app.embedder import Embedder
from app.ranker import rank_resumes

import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')


folder_path ="data/sample_resumes" 

resume_texts = extract_texts_from_folder(folder_path)

processed_resumes = {}

for name, text in resume_texts.items():
    processed_resumes[name] = clean_text(text)
    
# for name, text in processed_resumes.items():
#     print(f"\n====={name}======")
#     print(text[:1000])
resume_names = list(processed_resumes.keys())
resume_text_list = list(processed_resumes.values())

job_description = """
We are looking for a Python developer with experience in machine learning,
deep learning, and NLP. The candidate should have experience with
transformers and cloud deployment.
"""

processed_job_description = clean_text(job_description)

# print("\n===== JOB DESCRIPTION =====")
# print(processed_job_description)

embedder = Embedder()

resume_embeddings = embedder.embed_batch(list(processed_resumes.values()))
jd_embedding = embedder.embed_text(processed_job_description)

ranked_resumes = rank_resumes(resume_embeddings,resume_names,jd_embedding)

print("\n===== RANKED CANDIDATES =====")
for rank, (name, score) in enumerate(ranked_resumes, start=1):
    print(f"{rank}. {name} → Match Score: {score:.4f}")