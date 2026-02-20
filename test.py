from dotenv import load_dotenv
import os

from app.market_intelligence.role_detector import detect_role
from app.market_intelligence.web_retriever import retrieve_market_data
from app.market_intelligence.content_cleaner import clean_market_content
from app.market_intelligence.market_generator import MarketGenerator


# ---------------- LOAD ENV ----------------
load_dotenv()

print("GROQ TOKEN FOUND:", os.getenv("GROQ_API_KEY") is not None)


# ---------------- SAMPLE JD ----------------
jd = """
Job Title: Data Scientist

We are looking for a Data Scientist who will build machine learning
models, analyze large datasets and deploy scalable AI solutions.
"""


# ---------------- ROLE DETECTION ----------------
role = detect_role(jd)
print("\nDetected Role:", role)


# ---------------- WEB RETRIEVAL ----------------
print("\nRetrieving market data...")
raw_text = retrieve_market_data(role)

print("Raw text length:", len(raw_text))


# ---------------- CLEANING ----------------
print("\nCleaning content...")
cleaned_text = clean_market_content(raw_text)

print("Cleaned text length:", len(cleaned_text))


# ---------------- LLM GENERATION ----------------
print("\nGenerating Market Context using LLM...")

generator = MarketGenerator()

market_context = generator.generate_market_context(
    role,
    cleaned_text[:8000]  # safety truncation
)

print("\n=========== MARKET CONTEXT ===========\n")
print(market_context[:2000])