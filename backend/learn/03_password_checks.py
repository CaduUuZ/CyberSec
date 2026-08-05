# ============================================================
#  CARD 2 - PASSWORD STRENGTH CHECKER  |  Camada 1
#  Aula 03 - Condicionais (if/else) e regex (re)
# ============================================================
#
# Objetivo: dada uma senha, checar quais criterios ela cumpre
# e dar uma "nota" simples.

# 're' e o modulo de "expressoes regulares" (regex). Ja vem com
# o Python. Serve pra procurar PADROES dentro de um texto.
import re


# A senha que vamos analisar (troque a vontade e rode de novo).
senha = "Banana123"


# ------------------------------------------------------------
# PARTE 1 - Checando cada criterio (retorna True/False)
# ------------------------------------------------------------
#
# re.search(padrao, texto) procura o padrao no texto.
# - devolve um "match" (que vale True) se achou
# - devolve None (que vale False) se NAO achou
#
# Os padroes entre aspas usam "classes" entre colchetes [ ]:
#   [a-z]  -> qualquer letra minuscula de a ate z
#   [A-Z]  -> qualquer letra MAIUSCULA
#   [0-9]  -> qualquer digito de 0 a 9
#   [^A-Za-z0-9] -> qualquer coisa que NAO seja letra nem numero
#                   (ou seja: simbolos como ! @ # $ %). O '^' aqui
#                   dentro dos colchetes significa "o contrario de".

tem_minuscula = re.search(r"[a-z]", senha) is not None
tem_maiuscula = re.search(r"[A-Z]", senha) is not None
tem_numero    = re.search(r"[0-9]", senha) is not None
tem_simbolo   = re.search(r"[^A-Za-z0-9]", senha) is not None

# len(senha) conta quantos caracteres a senha tem.
tem_tamanho_bom = len(senha) >= 8

print(f"Analisando a senha: {senha}")
print(f"  Tem >= 8 caracteres? {tem_tamanho_bom}   (tem {len(senha)})")
print(f"  Tem minuscula?       {tem_minuscula}")
print(f"  Tem maiuscula?       {tem_maiuscula}")
print(f"  Tem numero?          {tem_numero}")
print(f"  Tem simbolo?         {tem_simbolo}")
print()


# ------------------------------------------------------------
# PARTE 2 - Somando uma "nota" de 0 a 5
# ------------------------------------------------------------
#
# Comecamos a nota em 0 e somamos 1 para cada criterio cumprido.
# Em Python, True vale 1 e False vale 0 numa soma -- mas aqui vou
# usar if para ficar bem explicito e voce ver o if funcionando.

nota = 0
if tem_tamanho_bom: nota = nota + 1
if tem_minuscula:   nota = nota + 1
if tem_maiuscula:   nota = nota + 1
if tem_numero:      nota = nota + 1
if tem_simbolo:     nota = nota + 1

print(f"Nota (0 a 5): {nota}")


# ------------------------------------------------------------
# PARTE 3 - Traduzindo a nota num rotulo (if / elif / else)
# ------------------------------------------------------------
#
# 'if' testa a primeira condicao. Se for falsa, 'elif' (else if)
# testa a proxima, e assim por diante. 'else' e o "se nada acima
# bateu". O Python para na PRIMEIRA condicao verdadeira.

if nota <= 1:
    rotulo = "Muito fraca"
elif nota == 2:
    rotulo = "Fraca"
elif nota == 3:
    rotulo = "Media"
elif nota == 4:
    rotulo = "Forte"
else:
    rotulo = "Muito forte"

print(f"Classificacao: {rotulo}")


# ------------------------------------------------------------
# PARTE 4 - Uma barrinha visual, so por diversao
# ------------------------------------------------------------
#
# "bloco cheio" repetido 'nota' vezes + "bloco vazio" o resto.
# O operador * repete um texto:  "ab" * 3  ->  "ababab"

barra = "#" * nota + "-" * (5 - nota)
print(f"Forca: [{barra}]")
