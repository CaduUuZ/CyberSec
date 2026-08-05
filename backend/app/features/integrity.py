# ============================================================
#  FEATURE: File Integrity Checker
#  O "cerebro" do Card 3: escanear uma pasta e comparar fotos.
# ============================================================

import hashlib
from pathlib import Path


def hash_do_arquivo(caminho: Path) -> str:
    """Calcula o SHA-256 dos bytes de um arquivo."""
    with open(caminho, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def escanear(pasta: str) -> dict:
    """Percorre a pasta (recursivo) e devolve {arquivo: hash}."""
    resultado = {}
    base = Path(pasta)

    for caminho in base.rglob("*"):
        if caminho.is_file():
            nome = str(caminho.relative_to(base))
            resultado[nome] = hash_do_arquivo(caminho)

    return resultado


def comparar(antigo: dict, novo: dict) -> dict:
    """Compara duas fotos e devolve o que mudou."""
    modificados = []
    adicionados = []
    removidos = []

    for nome, h in novo.items():
        if nome not in antigo:
            adicionados.append(nome)
        elif antigo[nome] != h:
            modificados.append(nome)

    for nome in antigo:
        if nome not in novo:
            removidos.append(nome)

    return {
        "modificados": modificados,
        "adicionados": adicionados,
        "removidos": removidos,
    }
