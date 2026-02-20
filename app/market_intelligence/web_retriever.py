from ddgs import DDGS
import requests
from bs4 import BeautifulSoup


MAX_RESULTS = 8
TIMEOUT = 10


def generate_search_queries(role: str):
    """
    Generate intelligent market queries for role.
    """

    queries = [
        f"{role} job market trends",
        f"{role} industry expectations",
        f"skills required for {role} today",
        f"{role} responsibilities in industry",
        f"future demand for {role}"
    ]

    return queries


def fetch_page_text(url: str):
    """
    Extract readable paragraph text from webpage.
    """

    try:
        response = requests.get(url, timeout=TIMEOUT)
        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = soup.find_all("p")

        text = " ".join(
            p.get_text(strip=True)
            for p in paragraphs
            if len(p.get_text()) > 50
        )

        return text

    except Exception:
        return ""


def retrieve_market_data(role: str):
    """
    Main retrieval pipeline.
    Returns aggregated market text.
    """

    collected_text = []

    queries = generate_search_queries(role)

    with DDGS() as ddgs:
        for query in queries:

            results = ddgs.text(query, max_results=MAX_RESULTS)

            for r in results:
                url = r.get("href")

                if not url:
                    continue

                page_text = fetch_page_text(url)

                if page_text:
                    collected_text.append(page_text)

    return "\n".join(collected_text)


