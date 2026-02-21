from app.market_intelligence.market_cache import (
    cache_exists,
    load_market_cache,
    save_market_cache
)

from app.market_intelligence.web_retriever import retrieve_market_data
from app.market_intelligence.content_cleaner import clean_market_content
from app.market_intelligence.market_generator import MarketGenerator


generator = MarketGenerator()


def get_market_context(role: str):

    # ---------- CACHE HIT ----------
    if cache_exists(role):
        print(f"[CACHE HIT] Loading market context for {role}")
        return load_market_cache(role)

    print(f"[CACHE MISS] Generating market context for {role}")

    # ---------- WEB RETRIEVAL ----------
    raw_text = retrieve_market_data(role)

    # ---------- CLEAN ----------
    cleaned_text = clean_market_content(raw_text)

    # ---------- LLM GENERATION ----------
    market_context = generator.generate_market_context(
        role,
        cleaned_text
    )

    # ---------- SAVE CACHE ----------
    save_market_cache(role, market_context)

    return market_context