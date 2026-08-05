# ============================================================
#  CARD 2 - PASSWORD STRENGTH CHECKER  |  Camada 1
#  Aula 04 - Entropia + juntar tudo numa funcao
# ============================================================

import re

# 'math' e o modulo de matematica do Python. Usamos math.log2,
# que calcula o logaritmo na base 2 (o "quantos bits" de algo).
import math


def analisar_senha(senha: str) -> dict:
    """Recebe uma senha e devolve um dicionario com a analise:
    criterios, tamanho do alfabeto, entropia, nota e rotulo.
    """

    # ---- 1) Checa os criterios (True/False), igual a aula 03 ----
    tem_minuscula = re.search(r"[a-z]", senha) is not None
    tem_maiuscula = re.search(r"[A-Z]", senha) is not None
    tem_numero    = re.search(r"[0-9]", senha) is not None
    tem_simbolo   = re.search(r"[^A-Za-z0-9]", senha) is not None

    # ---- 2) Calcula o tamanho do alfabeto (pool) ----
    # Comeca em 0 e soma o tamanho de cada conjunto que foi usado.
    pool = 0
    if tem_minuscula: pool += 26
    if tem_maiuscula: pool += 26
    if tem_numero:    pool += 10
    if tem_simbolo:   pool += 33

    # ---- 3) Calcula a entropia ----
    # Se a senha estiver vazia (ou pool 0), entropia e 0.
    if len(senha) == 0 or pool == 0:
        entropia = 0.0
    else:
        entropia = len(senha) * math.log2(pool)

    # round(x, 1) arredonda para 1 casa decimal (ex: 52.35 -> 52.4).
    entropia = round(entropia, 1)

    # ---- 4) Traduz a entropia num rotulo ----
    # Faixas usadas na pratica (aproximadas):
    if entropia < 28:
        rotulo = "Muito fraca"
        nota = 1
    elif entropia < 36:
        rotulo = "Fraca"
        nota = 2
    elif entropia < 60:
        rotulo = "Razoavel"
        nota = 3
    elif entropia < 128:
        rotulo = "Forte"
        nota = 4
    else:
        rotulo = "Muito forte"
        nota = 5

    # ---- 5) Devolve tudo num dicionario ----
    # Repare: um dicionario pode conter outro dicionario dentro
    # (aqui, "criterios" e um dicionario dentro do dicionario maior).
    return {
        "comprimento": len(senha),
        "alfabeto": pool,
        "entropia_bits": entropia,
        "nota": nota,
        "rotulo": rotulo,
        "criterios": {
            "minuscula": tem_minuscula,
            "maiuscula": tem_maiuscula,
            "numero": tem_numero,
            "simbolo": tem_simbolo,
            "tamanho_8": len(senha) >= 8,
        },
    }


# ------------------------------------------------------------
# Testando a funcao com varias senhas
# ------------------------------------------------------------
senhas_teste = ["123", "senha", "Banana123", "Banana123!", "S3nh@Muito+F0rte!2026"]

for s in senhas_teste:
    r = analisar_senha(s)
    barra = "#" * r["nota"] + "-" * (5 - r["nota"])
    print(f"{s:24} [{barra}]  {r['entropia_bits']:6} bits  ->  {r['rotulo']}")
