# ============================================================
#  FEATURE: Log Analyzer
#  O "cerebro" do Card 5: le o texto de um log de autenticacao
#  (formato auth.log/SSH) e devolve um relatorio de seguranca.
# ============================================================

import re
from collections import Counter

PADRAO_FALHA   = re.compile(r"Failed password for (\w+) from (\d+\.\d+\.\d+\.\d+)")
PADRAO_SUCESSO = re.compile(r"Accepted password for (\w+) from (\d+\.\d+\.\d+\.\d+)")
PADRAO_HORA    = re.compile(r"\d{2}:\d{2}:\d{2}")

LIMITE_FORCA_BRUTA = 5


def analisar_logs(texto: str) -> dict:
    """Recebe o texto de um log e devolve um relatorio de seguranca."""
    linhas = texto.splitlines()

    falhas_por_ip = Counter()
    usuarios_alvo = Counter()
    horas_de_falha = Counter()
    total_falhas = 0
    total_sucessos = 0

    for linha in linhas:
        falha = PADRAO_FALHA.search(linha)
        if falha:
            total_falhas += 1
            usuario, ip = falha.group(1), falha.group(2)
            falhas_por_ip[ip] += 1
            usuarios_alvo[usuario] += 1
            hora = PADRAO_HORA.search(linha)
            if hora:
                horas_de_falha[hora.group()[:2]] += 1
            continue

        if PADRAO_SUCESSO.search(linha):
            total_sucessos += 1

    suspeitos = [
        {"ip": ip, "falhas": qtd}
        for ip, qtd in falhas_por_ip.most_common()
        if qtd >= LIMITE_FORCA_BRUTA
    ]

    return {
        "total_linhas": len(linhas),
        "total_falhas": total_falhas,
        "total_sucessos": total_sucessos,
        "falhas_por_ip": [
            {"ip": ip, "falhas": q} for ip, q in falhas_por_ip.most_common()
        ],
        "usuarios_mais_tentados": [
            {"usuario": u, "tentativas": q} for u, q in usuarios_alvo.most_common(5)
        ],
        "falhas_por_hora": dict(horas_de_falha),
        "suspeitos": suspeitos,
    }
