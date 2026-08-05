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
