# ============================================================
#  CARD 5 - LOG ANALYZER  |  Camada 1 (parte B)
#  Aula 10 - Juntar tudo numa funcao analisar_logs(texto)
# ============================================================

import re
from collections import Counter


# Padroes (compilados uma vez). Grupos capturam usuario, ip e hora.
#   A hora vem do inicio: "Aug  5 03:11:01" -> pegamos "03".
PADRAO_FALHA   = re.compile(r"Failed password for (\w+) from (\d+\.\d+\.\d+\.\d+)")
PADRAO_SUCESSO = re.compile(r"Accepted password for (\w+) from (\d+\.\d+\.\d+\.\d+)")
PADRAO_HORA    = re.compile(r"\d{2}:\d{2}:\d{2}")   # ex: 03:11:01

LIMITE_FORCA_BRUTA = 5


def analisar_logs(texto: str) -> dict:
    """Recebe o texto de um log e devolve um relatorio de seguranca."""
    linhas = texto.splitlines()   # quebra o texto em linhas

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

            # Pega a hora (os 2 primeiros digitos do horario).
            hora = PADRAO_HORA.search(linha)
            if hora:
                # hora.group() = "03:11:01" -> [:2] = "03"
                horas_de_falha[hora.group()[:2]] += 1
            continue   # ja tratou esta linha, vai pra proxima

        if PADRAO_SUCESSO.search(linha):
            total_sucessos += 1

    # Monta a lista de suspeitos (IPs acima do limite).
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


# ------------------------------------------------------------
# Testando: lemos o arquivo e passamos o TEXTO pra funcao
# ------------------------------------------------------------
with open("demo_logs/auth.log", "r") as f:
    conteudo = f.read()

rel = analisar_logs(conteudo)

print("=== RELATORIO DE SEGURANCA ===")
print(f"Linhas: {rel['total_linhas']} | Falhas: {rel['total_falhas']} | Sucessos: {rel['total_sucessos']}")
print()
print("Falhas por IP:")
for item in rel["falhas_por_ip"]:
    print(f"  {item['ip']:16} -> {item['falhas']}")
print()
print("Usuarios mais tentados:")
for item in rel["usuarios_mais_tentados"]:
    print(f"  {item['usuario']:10} -> {item['tentativas']}")
print()
print("Falhas por hora:", rel["falhas_por_hora"])
print()
print("SUSPEITOS (forca bruta):")
for s in rel["suspeitos"]:
    print(f"  ALERTA! {s['ip']} ({s['falhas']} falhas)")
