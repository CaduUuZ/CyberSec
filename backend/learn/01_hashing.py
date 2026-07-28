# ============================================================
#  CARD 1 - HASH GENERATOR  |  Camada 1: Python puro
#  Aula 01 - Entendendo hashlib
# ============================================================
#
# Objetivo: entender como gerar um hash em Python.
# Rode este arquivo no terminal e leia a saida com calma.

# 'hashlib' e um modulo que ja vem junto com o Python (nao
# precisa instalar nada). Ele contem os algoritmos de hash.
import hashlib


# ------------------------------------------------------------
# PARTE 1 - O hash mais basico possivel
# ------------------------------------------------------------

texto = "senha123"

# Computadores nao dao hash de "texto", eles dao hash de BYTES.
# Entao primeiro convertemos o texto em bytes com .encode().
# "utf-8" e so o "idioma" de conversao (o padrao mundial).
texto_em_bytes = texto.encode("utf-8")

# Agora criamos o hash SHA-256 desses bytes.
# .hexdigest() transforma o resultado num texto legivel (hexadecimal).
hash_resultado = hashlib.sha256(texto_em_bytes).hexdigest()

print("PARTE 1 - hash basico")
print(f"  Texto original: {texto}")
print(f"  Hash SHA-256:   {hash_resultado}")
print()


# ------------------------------------------------------------
# PARTE 2 - Propriedade: DETERMINISTICO
# A mesma entrada gera SEMPRE o mesmo hash.
# ------------------------------------------------------------

hash_a = hashlib.sha256("banana".encode("utf-8")).hexdigest()
hash_b = hashlib.sha256("banana".encode("utf-8")).hexdigest()

print("PARTE 2 - deterministico")
print(f"  hash_a == hash_b ? {hash_a == hash_b}")  # deve dar True
print()


# ------------------------------------------------------------
# PARTE 3 - Propriedade: EFEITO AVALANCHE
# Mudar UMA letra muda o hash inteiro.
# ------------------------------------------------------------

hash1 = hashlib.sha256("banana".encode("utf-8")).hexdigest()
hash2 = hashlib.sha256("Banana".encode("utf-8")).hexdigest()  # so o "B" maiusculo

print("PARTE 3 - efeito avalanche")
print(f"  'banana' -> {hash1}")
print(f"  'Banana' -> {hash2}")
print(f"  Sao iguais? {hash1 == hash2}")  # deve dar False
print()


# ------------------------------------------------------------
# PARTE 4 - Varios algoritmos de uma vez
# O card final vai mostrar MD5, SHA1, SHA256 e SHA512 juntos.
# ------------------------------------------------------------

texto = "hello"
dados = texto.encode("utf-8")

print("PARTE 4 - varios algoritmos para 'hello'")
print(f"  MD5:    {hashlib.md5(dados).hexdigest()}")
print(f"  SHA1:   {hashlib.sha1(dados).hexdigest()}")
print(f"  SHA256: {hashlib.sha256(dados).hexdigest()}")
print(f"  SHA512: {hashlib.sha512(dados).hexdigest()}")
print()

# Repare que MD5 e curtinho e SHA512 e longo.
# Quanto maior/mais novo o algoritmo, mais seguro.
# MD5 e SHA1 sao considerados QUEBRADOS hoje (nao use pra senha!),
# mas ainda aparecem para checar integridade de arquivos.
