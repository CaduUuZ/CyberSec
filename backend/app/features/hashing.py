# ============================================================
#  FEATURE: Hash Generator
#  O "cerebro" do Card 1. Mesma funcao que voce escreveu na
#  aula 02, agora no lugar oficial do projeto.
# ============================================================

import hashlib


def gerar_hashes(texto: str) -> dict:
    """Recebe um texto e devolve um dicionario com os 4 hashes.

    O ': str' e o '-> dict' sao "dicas de tipo" (type hints):
    avisam que a entrada e um texto e a saida e um dicionario.
    Nao sao obrigatorios, mas deixam o codigo claro e ajudam
    o FastAPI a montar a documentacao automatica.
    """
    dados = texto.encode("utf-8")

    return {
        "md5":    hashlib.md5(dados).hexdigest(),
        "sha1":   hashlib.sha1(dados).hexdigest(),
        "sha256": hashlib.sha256(dados).hexdigest(),
        "sha512": hashlib.sha512(dados).hexdigest(),
    }
