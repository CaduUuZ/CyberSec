# ============================================================
#  CARD 3 - FILE INTEGRITY CHECKER  |  Camada 1 (parte A)
#  Aula 05 - Ler arquivos do disco e salvar/carregar JSON
# ============================================================

import hashlib
import json   # modulo pra trabalhar com JSON (ja vem no Python)


# ------------------------------------------------------------
# PARTE 1 - Hashear um ARQUIVO (nao um texto)
# ------------------------------------------------------------
#
# Pra hashear um arquivo, a gente le os BYTES dele do disco.
#
#   open(caminho, "rb")  abre o arquivo:
#     "r" = read (ler),  "b" = binary (bytes crus)
#
#   'with' e a forma segura de abrir arquivos: ele FECHA o
#   arquivo sozinho no fim do bloco, mesmo se der erro.

def hash_do_arquivo(caminho: str) -> str:
    with open(caminho, "rb") as f:   # abre o arquivo
        conteudo = f.read()          # le todos os bytes
    return hashlib.sha256(conteudo).hexdigest()


print("PARTE 1 - hash de cada arquivo da pasta demo")
for nome in ["config.txt", "usuarios.txt", "log.txt"]:
    caminho = "demo/" + nome
    print(f"  {nome:14} -> {hash_do_arquivo(caminho)}")
print()


# ------------------------------------------------------------
# PARTE 2 - Salvar dados num arquivo JSON
# ------------------------------------------------------------
#
# JSON e um formato de texto pra guardar dados (o mesmo que a
# API usa!). Um dicionario Python vira JSON e volta facilmente.

# Montamos um dicionario {nome_do_arquivo: hash}
baseline = {}
for nome in ["config.txt", "usuarios.txt", "log.txt"]:
    baseline[nome] = hash_do_arquivo("demo/" + nome)

# json.dump escreve o dicionario num arquivo de texto.
#   indent=2  deixa o JSON "bonito" (identado, legivel)
with open("demo_baseline.json", "w") as f:
    json.dump(baseline, f, indent=2)

print("PARTE 2 - baseline salvo em demo_baseline.json")
print()


# ------------------------------------------------------------
# PARTE 3 - Carregar de volta o JSON
# ------------------------------------------------------------
#
# json.load le um arquivo JSON e devolve o dicionario de volta.

with open("demo_baseline.json", "r") as f:
    carregado = json.load(f)

print("PARTE 3 - baseline carregado do disco:")
for nome, h in carregado.items():
    print(f"  {nome:14} -> {h[:16]}...")   # mostra so os 16 primeiros
