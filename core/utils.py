import unicodedata
import re

def normalizar(texto: str) -> str:
    # Remove acentos
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")

    # torna maiúsculas
    texto = texto.lower()

    # Mantém apenas letras A–Z e espaços
    texto = re.sub(r"[^a-z ]", "", texto)

    return texto