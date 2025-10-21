from pathlib import Path
import shutil

# caminho base (a própria pasta onde o script está)
path_base = Path(__file__).parent

# percorre todos os arquivos .txt nas subpastas
for arquivo in sorted(path_base.rglob("*.txt")):
    # ignora os arquivos que já estão diretamente em data/
    if arquivo.parent == path_base:
        continue

    # nome base do arquivo (sem o caminho)
    nome = arquivo.name
    nome = arquivo.name.removesuffix(".txt") + "_" + arquivo.parent.name + ".txt"

    # destino: pasta data/
    destino = path_base / nome


    # copia o arquivo (pode trocar por .move se quiser mover)
    shutil.copy(arquivo, destino)
    print(f"Copiado: {arquivo} -> {destino}")
