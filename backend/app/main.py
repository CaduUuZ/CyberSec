# ============================================================
#  API PRINCIPAL - CyberSec Toolkit
#  Camada 2: aqui os endpoints "ligam os fios" entre o
#  navegador (React) e as funcoes em features/.
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Importamos NOSSAS funcoes das features.
from app.features.hashing import gerar_hashes
from app.features.password import analisar_senha
from app.features.integrity import escanear, comparar
from app.features.scanner import escanear as escanear_portas

# 'Path' aqui e do Python (pathlib), pra checar se a pasta existe.
from pathlib import Path

# socket -> resolver o host;  time -> cronometrar o scan.
import socket
import time


# 1) Cria a aplicacao. 'title' aparece na documentacao automatica.
app = FastAPI(title="CyberSec Toolkit API")


# 2) CORS: por seguranca, o navegador bloqueia um site de chamar
#    uma API de "endereco diferente". O React vai rodar na porta
#    5173 e a API na 8000 -> enderecos diferentes. Esta config
#    autoriza o React a conversar com a API. (Deixamos liberado
#    para desenvolvimento; em producao a gente restringe.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# 3) Pydantic: descreve o formato dos dados que o site vai ENVIAR.
#    Aqui dizemos "o site precisa mandar um campo 'texto' que e string".
#    Se mandar errado, o FastAPI recusa sozinho com uma mensagem clara.
class HashRequest(BaseModel):
    texto: str


# Formato dos dados que o site envia para o Card 2 (a senha).
class PasswordRequest(BaseModel):
    senha: str


# Card 3: para criar a baseline, o site manda so a pasta.
class BaselineRequest(BaseModel):
    pasta: str


# Card 3: para verificar, o site manda a pasta E a foto antiga.
# dict[str, str] = um dicionario de {nome_do_arquivo: hash}.
class VerifyRequest(BaseModel):
    pasta: str
    baseline: dict[str, str]


# Card 4: host e faixa de portas a escanear.
class ScanRequest(BaseModel):
    host: str
    inicio: int = 1
    fim: int = 1024


# 4) Primeiro endpoint: a rota inicial "/", so pra testar se a API vive.
#    O @app.get("/") e um "decorator": ele PLUGA a funcao abaixo na
#    rota "/". Quando alguem acessa "/", o FastAPI chama esta funcao.
@app.get("/")
def raiz():
    return {"status": "ok", "mensagem": "API do CyberSec Toolkit rodando!"}


# 5) O endpoint do Card 1.
#    @app.post -> recebe DADOS do site (a senha/texto a ser hasheado).
#    "/api/hash" -> o endereco desse recurso.
@app.post("/api/hash")
def endpoint_hash(req: HashRequest):
    # req.texto e o texto que o site mandou (validado pelo Pydantic).
    # Chamamos nossa funcao e devolvemos o resultado.
    resultado = gerar_hashes(req.texto)

    # Um dicionario retornado vira JSON automaticamente. Adicionamos
    # tambem o texto original pra ficar completo na resposta.
    return {
        "texto": req.texto,
        "hashes": resultado,
    }


# 6) O endpoint do Card 2 - Password Strength Checker.
@app.post("/api/password")
def endpoint_password(req: PasswordRequest):
    # Chama nossa funcao e devolve a analise. Como ela ja retorna
    # um dicionario completo, e so entregar direto.
    return analisar_senha(req.senha)


# 7) Card 3 - criar a baseline (a "foto" de uma pasta).
@app.post("/api/integrity/baseline")
def endpoint_baseline(req: BaselineRequest):
    # Antes de escanear, conferimos se a pasta existe de verdade.
    if not Path(req.pasta).is_dir():
        return {"erro": f"Pasta nao encontrada: {req.pasta}"}

    foto = escanear(req.pasta)
    return {
        "pasta": req.pasta,
        "total": len(foto),   # quantos arquivos foram fotografados
        "baseline": foto,
    }


# 8) Card 3 - verificar a integridade (comparar com a foto antiga).
@app.post("/api/integrity/verify")
def endpoint_verify(req: VerifyRequest):
    if not Path(req.pasta).is_dir():
        return {"erro": f"Pasta nao encontrada: {req.pasta}"}

    atual = escanear(req.pasta)
    return comparar(req.baseline, atual)


# 9) Card 4 - Port Scanner.
@app.post("/api/scan")
def endpoint_scan(req: ScanRequest):
    # --- Validacoes de seguranca / sanidade ---
    if req.inicio < 1 or req.fim > 65535 or req.inicio > req.fim:
        return {"erro": "Faixa invalida. Use portas entre 1 e 65535."}

    # Limite: no maximo 2000 portas por scan (evita scan gigante).
    if (req.fim - req.inicio + 1) > 2000:
        return {"erro": "Faixa muito grande. Maximo de 2000 portas por vez."}

    # Resolve o host (transforma nome em IP). Se falhar, o host
    # nao existe / nao foi encontrado.
    try:
        ip = socket.gethostbyname(req.host)
    except socket.gaierror:
        return {"erro": f"Host nao encontrado: {req.host}"}

    # --- Roda o scan e cronometra ---
    t0 = time.time()
    abertas = escanear_portas(ip, req.inicio, req.fim)
    segundos = round(time.time() - t0, 2)

    return {
        "host": req.host,
        "ip": ip,
        "faixa": f"{req.inicio}-{req.fim}",
        "segundos": segundos,
        "abertas": abertas,
    }
