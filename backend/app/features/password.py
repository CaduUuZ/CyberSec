# ============================================================
#  FEATURE: Password Strength Checker
#  O "cerebro" do Card 2. Mesma funcao da aula 04, agora no
#  lugar oficial do projeto.
# ============================================================

import re
import math


def analisar_senha(senha: str) -> dict:
    """Recebe uma senha e devolve a analise completa:
    criterios cumpridos, tamanho do alfabeto, entropia, nota e rotulo.
    """
    tem_minuscula = re.search(r"[a-z]", senha) is not None
    tem_maiuscula = re.search(r"[A-Z]", senha) is not None
    tem_numero    = re.search(r"[0-9]", senha) is not None
    tem_simbolo   = re.search(r"[^A-Za-z0-9]", senha) is not None

    pool = 0
    if tem_minuscula: pool += 26
    if tem_maiuscula: pool += 26
    if tem_numero:    pool += 10
    if tem_simbolo:   pool += 33

    if len(senha) == 0 or pool == 0:
        entropia = 0.0
    else:
        entropia = round(len(senha) * math.log2(pool), 1)

    if entropia < 28:
        rotulo, nota = "Muito fraca", 1
    elif entropia < 36:
        rotulo, nota = "Fraca", 2
    elif entropia < 60:
        rotulo, nota = "Razoavel", 3
    elif entropia < 128:
        rotulo, nota = "Forte", 4
    else:
        rotulo, nota = "Muito forte", 5

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
