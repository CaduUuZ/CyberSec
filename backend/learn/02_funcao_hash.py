# ============================================================
#  CARD 1 - HASH GENERATOR  |  Camada 1: Python puro
#  Aula 02 - Funcoes e dicionarios
# ============================================================
#
# Objetivo: pegar o codigo repetido da aula 01 e transformar
# numa FUNCAO reutilizavel que devolve um DICIONARIO.

import hashlib


# ------------------------------------------------------------
# DEFININDO UMA FUNCAO
# ------------------------------------------------------------
#
#   def  -> palavra-chave que diz "estou criando uma funcao"
#   gerar_hashes -> o nome que eu escolhi pra funcao
#   (texto) -> a ENTRADA (chamamos de "parametro")
#   :  -> abre o bloco da funcao
#   tudo que fica INDENTADO abaixo pertence a funcao
#
def gerar_hashes(texto):
    # 1) Converte o texto em bytes (igual na aula 01)
    dados = texto.encode("utf-8")

    # 2) Monta um DICIONARIO com os 4 algoritmos.
    #    Formato ->  "chave": valor
    resultado = {
        "md5":    hashlib.md5(dados).hexdigest(),
        "sha1":   hashlib.sha1(dados).hexdigest(),
        "sha256": hashlib.sha256(dados).hexdigest(),
        "sha512": hashlib.sha512(dados).hexdigest(),
    }

    # 3) 'return' devolve o resultado pra quem chamou a funcao.
    #    Sem return, a funcao nao entrega nada.
    return resultado


# ------------------------------------------------------------
# USANDO (CHAMANDO) A FUNCAO
# ------------------------------------------------------------

# Chamamos a funcao passando "hello". O que ela retornar
# fica guardado na variavel 'hashes'.
hashes = gerar_hashes("hello")

print("Retorno da funcao (um dicionario):")
print(hashes)
print()

# Pra pegar UM valor do dicionario, usamos a chave entre colchetes:
print("Pegando so o SHA-256 pela chave:")
print(f"  {hashes['sha256']}")
print()

# E a beleza da funcao: reusar com QUALQUER entrada, sem repetir codigo.
print("Reusando a funcao com outras entradas:")
for palavra in ["banana", "senha123", "DieselSquid"]:
    resultado = gerar_hashes(palavra)
    print(f"  {palavra:12} -> SHA-256: {resultado['sha256']}")
