# ============================================================
#  FEATURE: Port Scanner
#  O "cerebro" do Card 4: escaneia uma faixa de portas de um host.
#  ETICA: use apenas em sistemas seus ou com autorizacao.
# ============================================================

import socket
from concurrent.futures import ThreadPoolExecutor

# Numero da porta -> nome do servico mais comum.
SERVICOS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 135: "MSRPC", 139: "NetBIOS",
    143: "IMAP", 443: "HTTPS", 445: "SMB", 3306: "MySQL",
    3389: "RDP", 5432: "PostgreSQL", 5900: "VNC", 6379: "Redis",
    8000: "HTTP-alt", 8080: "HTTP-proxy", 27017: "MongoDB",
}


def checar_porta(host: str, porta: int, timeout: float) -> int | None:
    """Devolve o numero da porta se aberta, ou None se fechada."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    aberta = s.connect_ex((host, porta)) == 0
    s.close()
    return porta if aberta else None


def escanear(host: str, inicio: int, fim: int, timeout: float = 0.3) -> list:
    """Escaneia host de 'inicio' a 'fim'. Devolve lista de dicts
    [{porta, servico}, ...] apenas com as portas abertas."""
    abertas = []

    with ThreadPoolExecutor(max_workers=300) as pool:
        resultados = pool.map(
            lambda p: checar_porta(host, p, timeout),
            range(inicio, fim + 1),
        )
        for porta in resultados:
            if porta is not None:
                abertas.append({
                    "porta": porta,
                    "servico": SERVICOS.get(porta, "desconhecido"),
                })

    # Ordena pela porta (o parametro key diz "ordene por este campo").
    return sorted(abertas, key=lambda item: item["porta"])
