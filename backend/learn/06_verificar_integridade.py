# ============================================================
#  CARD 3 - FILE INTEGRITY CHECKER  |  Camada 1 (parte B)
#  Aula 06 - Percorrer pastas (pathlib) e detectar mudancas
# ============================================================

import hashlib
import shutil                 # copiar/remover pastas e arquivos
from pathlib import Path      # jeito moderno de lidar com caminhos


# Reaproveitamos a ideia do Card 1: hash de bytes.
def hash_do_arquivo(caminho: Path) -> str:
    with open(caminho, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


# ------------------------------------------------------------
# escanear(): percorre a pasta e devolve {arquivo: hash}
# ------------------------------------------------------------
def escanear(pasta: str) -> dict:
    resultado = {}
    base = Path(pasta)

    # .rglob("*") percorre a pasta RECURSIVAMENTE (inclui subpastas)
    # e devolve todos os caminhos encontrados.
    for caminho in base.rglob("*"):
        # so queremos ARQUIVOS (pular pastas).
        if caminho.is_file():
            # .relative_to(base) guarda o nome "curto" (sem o caminho
            # todo), pra chave ficar limpa: "config.txt" em vez de
            # "demo_trabalho/config.txt".
            nome = str(caminho.relative_to(base))
            resultado[nome] = hash_do_arquivo(caminho)

    return resultado


# ------------------------------------------------------------
# comparar(): descobre o que mudou entre duas fotos
# ------------------------------------------------------------
def comparar(antigo: dict, novo: dict) -> dict:
    modificados = []
    adicionados = []
    removidos = []

    # Arquivos que existem na foto NOVA
    for nome, h in novo.items():
        if nome not in antigo:
            adicionados.append(nome)          # nao existia antes
        elif antigo[nome] != h:
            modificados.append(nome)          # existia, mas o hash mudou

    # Arquivos que existiam na foto ANTIGA e sumiram
    for nome in antigo:
        if nome not in novo:
            removidos.append(nome)

    return {
        "modificados": modificados,
        "adicionados": adicionados,
        "removidos": removidos,
    }


# ============================================================
#  DEMONSTRACAO (roda automatica)
# ============================================================

# 1) Fazemos uma copia da pasta demo pra nao mexer nos originais.
#    Se a copia ja existir de uma execucao anterior, apagamos.
if Path("demo_trabalho").exists():
    shutil.rmtree("demo_trabalho")
shutil.copytree("demo", "demo_trabalho")

# 2) Tiramos a FOTO inicial (o estado confiavel).
baseline = escanear("demo_trabalho")
print("Foto inicial (baseline):")
for nome in baseline:
    print(f"  {nome}")
print()

# 3) Simulamos um ataque na pasta:
print("== Simulando um ataque... ==")
#   a) altera um arquivo existente (adiciona uma linha)
with open("demo_trabalho/config.txt", "a") as f:
    f.write("porta=31337\n")
print("  - config.txt foi ALTERADO")
#   b) deleta um arquivo
Path("demo_trabalho/log.txt").unlink()
print("  - log.txt foi DELETADO")
#   c) cria um arquivo malicioso novo
with open("demo_trabalho/backdoor.txt", "w") as f:
    f.write("codigo malicioso aqui\n")
print("  - backdoor.txt foi CRIADO")
print()

# 4) Tiramos a foto ATUAL e comparamos com a baseline.
atual = escanear("demo_trabalho")
resultado = comparar(baseline, atual)

print("== Resultado da verificacao de integridade ==")
print(f"  MODIFICADOS: {resultado['modificados']}")
print(f"  ADICIONADOS: {resultado['adicionados']}")
print(f"  REMOVIDOS:   {resultado['removidos']}")
