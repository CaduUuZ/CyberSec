# ============================================================
#  CARD 4 - PORT SCANNER  |  Camada 1 (parte A)
#  Aula 07 - Sockets: checar se UMA porta esta aberta
# ============================================================
#
# ETICA: so escaneie sistemas seus ou com autorizacao.
# Aqui usamos 127.0.0.1 (localhost = sua propria maquina).

# 'socket' e o modulo de rede do Python (ja vem incluso).
# Um socket e como um "telefone": seu programa liga para um
# host:porta e ve se alguem atende.
import socket


def porta_aberta(host: str, porta: int, timeout: float = 0.5) -> bool:
    """Tenta conectar em host:porta. Devolve True se estiver aberta."""

    # Cria o socket.
    #   AF_INET     -> usar IPv4 (enderecos tipo 127.0.0.1)
    #   SOCK_STREAM -> usar TCP (conexao confiavel)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Quanto tempo esperar antes de desistir (em segundos).
    # Sem isso, uma porta "morta" poderia travar por muito tempo.
    s.settimeout(timeout)

    # connect_ex tenta conectar e devolve um CODIGO:
    #   0     -> conectou! a porta esta ABERTA
    #   outro -> nao conectou (fechada, filtrada, etc.)
    # (Usamos connect_ex em vez de connect porque ele devolve um
    #  numero em vez de estourar um erro -- mais facil de tratar.)
    codigo = s.connect_ex((host, porta))

    # Sempre fechar o socket quando terminar (liberar o "telefone").
    s.close()

    return codigo == 0


# ------------------------------------------------------------
# Testando em algumas portas do localhost
# ------------------------------------------------------------
host = "127.0.0.1"

# 8000 = nossa API FastAPI  |  5173 = nosso frontend Vite
# 9999 = provavelmente nada rodando (deve dar fechada)
for porta in [8000, 5173, 9999]:
    if porta_aberta(host, porta):
        print(f"  Porta {porta}: ABERTA")
    else:
        print(f"  Porta {porta}: fechada")
