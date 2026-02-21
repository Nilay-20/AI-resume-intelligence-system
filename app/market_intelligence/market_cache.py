import os


BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)

CACHE_DIR = os.path.join(BASE_DIR, "market_cache")

def normalize_role(role: str) -> str:
    """
    Convert role into safe filename.
    """
    return role.lower().replace(" ", "_")


def get_cache_path(role: str):

    filename = normalize_role(role) + ".txt"
    return os.path.join(CACHE_DIR, filename)


def cache_exists(role: str) -> bool:
    """
    Check if market context already cached.
    """
    return os.path.exists(get_cache_path(role))


def load_market_cache(role: str) -> str:
    """
    Load cached market context.
    """
    path = get_cache_path(role)

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def save_market_cache(role: str, content: str):
    """
    Save generated market context.
    """

    os.makedirs(CACHE_DIR, exist_ok=True)

    path = get_cache_path(role)
    print("Saving cache at:", os.path.abspath(path)) 
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)