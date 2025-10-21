import unicodedata
import re
from pathlib import Path

def normalizar(texto: str) -> str:
    # Remove acentos
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")

    # torna minúsculas
    texto = texto.lower()

    # Mantém apenas letras a–z e espaços
    texto = re.sub(r"[^a-z 0-9\n]", "", texto)

    return texto

def verificarModelo(entrada: str) -> bool:
    if (" ") in entrada:
        print("Digite apenas uma palavra!")
        return False

def existeDisco():
    caminho = Path("../index_storage/disk.json")

    if caminho.is_file():
        return True
    else:
        return False