import re
import unicodedata
from pathlib import Path


def normalize(text: str) -> str:
    # Remove acentos
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")

    text = text.lower()
    text = re.sub(r"[^a-z 0-9\n]", "", text)

    return text

def disk_exists() -> bool:
    path = Path("index_storage/disk.json")
    return path.is_file()
