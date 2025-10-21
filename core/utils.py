import unicodedata
import re
from pathlib import Path


def normalize(text: str) -> str:
    """Removes accents, converts to lowercase, and keeps only letters, digits, and spaces."""
    # Remove accents
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")

    # Convert to lowercase
    text = text.lower()

    # Keep only letters a–z, digits, and spaces
    text = re.sub(r"[^a-z 0-9\n]", "", text)

    return text


def validate_input(entry: str) -> bool:
    """Checks if the input contains only one word."""
    if " " in entry:
        print("Please enter only one word!")
        return False
    return True


def disk_exists() -> bool:
    """Checks whether the disk.json file exists in the index_storage folder."""
    path = Path("../index_storage/disk.json")
    return path.is_file()
