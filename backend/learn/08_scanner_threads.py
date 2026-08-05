# ============================================================
#  CARD 4 - PORT SCANNER  |  Camada 1 (parte B)
#  Aula 08 - Escanear uma FAIXA de portas usando threads
# ============================================================
#
# ETICA: so escaneie sistemas seus ou com autorizacao.

import socket
import time

# ThreadPoolExecutor: um "gerente" que distribui tarefas entre
# varias threads (linhas de execucao paralelas). Assim checamos
# muitas portas ao mesmo tempo em vez de uma por vez.
from concurrent.futures import ThreadPoolExecutor


# Dicionario "numero da porta -> nome do servico" (os mais comuns).
SERVICOS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS",
    3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 8000: "HTTP-alt",
    8080: "HTTP-proxy",
}


def checar_porta(host: str, porta: int, timeout: float = 0.5):
    """Devolve a porta se estiver aberta, ou None se fechada."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    aberta = s.connect_ex((host, porta)) == 0
    s.close()
    return porta if aberta else None


def escanear(host: str, inicio: int, fim: int) -> list:
    """Escaneia de 'inicio' ate 'fim' e devolve a lista de portas abertas."""
    abertas = []

    # 'with' cria o pool e o fecha no fim. max_workers = quantas
    # threads rodam ao mesmo tempo (100 checagens simultaneas).
    with ThreadPoolExecutor(max_workers=100) as pool:
        # pool.map roda checar_porta(host, p) para cada porta p da faixa,
        # distribuindo entre as threads. range(inicio, fim+1) gera os
        # numeros de inicio ate fim (inclusive).
        for resultado in pool.map(lambda p: checar_porta(host, p),
                                  range(inicio, fim + 1)):
            if resultado is not None:
                abertas.append(resultado)

    return sorted(abertas)


# ------------------------------------------------------------
# Escaneando o localhost, portas 1 a 9000
# ------------------------------------------------------------
host = "127.0.0.1"
inicio, fim = 1, 9000

print(f"Escaneando {host} (portas {inicio}-{fim})...")

# Cronometramos pra ver a velocidade das threads.
t0 = time.time()
portas_abertas = escanear(host, inicio, fim)
segundos = round(time.time() - t0, 2)

print(f"Concluido em {segundos}s. Portas abertas:")
if not portas_abertas:
    print("  (nenhuma)")
for p in portas_abertas:
    servico = SERVICOS.get(p, "desconhecido")   # .get evita erro se nao achar
    print(f"  {p:5}  {servico}")
