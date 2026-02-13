from app.parser import extract_texts_from_folder
from app.processor import clean_text
import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')


folder_path ="data/sample_resumes" 

resume_texts = extract_texts_from_folder(folder_path)

processed_resumes = {}

for name, text in resume_texts.items():
    processed_resumes[name] = clean_text(text)
    
for name, text in processed_resumes.items():
    print(f"\n====={name}======")
    print(text[:1000])

job_description = """
We are looking for a Python developer with experience in machine learning,
deep learning, and NLP. The candidate should have experience with
transformers and cloud deployment.
"""

processed_job_description = clean_text(job_description)

print("\n===== JOB DESCRIPTION =====")
print(processed_job_description)