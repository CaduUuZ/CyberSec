# ============================================================
#  CARD 5 - LOG ANALYZER  |  Camada 1 (parte A)
#  Aula 09 - Regex com grupos + contar com Counter
# ============================================================

import re

# 'Counter' e um contador pronto: voce joga itens nele e ele
# conta quantas vezes cada um apareceu. Vem em 'collections'.
from collections import Counter


# ------------------------------------------------------------
# PARTE 1 - Ler o log e olhar linha por linha
# ------------------------------------------------------------
with open("demo_logs/auth.log", "r") as f:
    linhas = f.readlines()   # devolve uma lista: cada item = 1 linha

print(f"O log tem {len(linhas)} linhas.\n")


# ------------------------------------------------------------
# PARTE 2 - Regex com GRUPOS pra extrair dados
# ------------------------------------------------------------
#
# Ate agora usamos regex so pra dizer "tem ou nao tem".
# Agora vamos EXTRAIR pedacos usando GRUPOS -- os parenteses ( ).
# Cada par de parenteses captura um pedaco que a gente pega depois.
#
# Padrao que queremos casar (nas linhas de falha):
#   Failed password for <usuario> from <ip> ...
#
#   (\w+)                     -> grupo 1: o usuario (uma palavra)
#   (\d+\.\d+\.\d+\.\d+)      -> grupo 2: o IP (4 numeros com pontos)
#
#   \d+  = um ou mais digitos     \.  = um ponto literal
#   \w+  = uma ou mais letras/numeros/underscore

padrao_falha = re.compile(r"Failed password for (\w+) from (\d+\.\d+\.\d+\.\d+)")

print("PARTE 2 - extraindo usuario e IP das falhas:")
for linha in linhas:
    m = padrao_falha.search(linha)
    if m:                      # se a linha casou com o padrao
        usuario = m.group(1)   # grupo 1 = usuario
        ip = m.group(2)        # grupo 2 = IP
        print(f"  falha: usuario={usuario:10} ip={ip}")
print()


# ------------------------------------------------------------
# PARTE 3 - Contar falhas por IP com Counter
# ------------------------------------------------------------
contador_ips = Counter()

for linha in linhas:
    m = padrao_falha.search(linha)
    if m:
        ip = m.group(2)
        contador_ips[ip] += 1   # soma 1 para aquele IP

print("PARTE 3 - falhas por IP (do maior para o menor):")
# .most_common() ja devolve ordenado do que mais aparece pro que menos.
for ip, qtd in contador_ips.most_common():
    print(f"  {ip:16} -> {qtd} falhas")
print()


# ------------------------------------------------------------
# PARTE 4 - Sinalizar forca bruta (acima de um limite)
# ------------------------------------------------------------
LIMITE = 5   # 5+ falhas do mesmo IP = suspeito

print(f"PARTE 4 - IPs suspeitos (>= {LIMITE} falhas):")
for ip, qtd in contador_ips.most_common():
    if qtd >= LIMITE:
        print(f"  ALERTA! {ip} tentou {qtd} vezes (possivel forca bruta)")
