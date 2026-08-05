// ============================================================
//  CARD 3 - File Integrity Checker (frontend)
//  Fluxo de 2 passos: criar baseline -> verificar mudancas.
// ============================================================

import { useState } from "react";

const API = "http://127.0.0.1:8000";

// Caminho da pasta de teste, so pra facilitar (o usuario pode trocar).
const PASTA_EXEMPLO =
  "C:/Users/Cadu F. Paiva/Documents/GitHub/DieselSquid/CyberSec/backend/learn/demo";

export default function FileIntegrityCard() {
  const [aberto, setAberto] = useState(false);
  const [pasta, setPasta] = useState("");
  const [baseline, setBaseline] = useState(null); // a "foto" guardada
  const [total, setTotal] = useState(0);           // quantos arquivos
  const [diff, setDiff] = useState(null);          // resultado da verificacao
  const [erro, setErro] = useState("");

  // Passo 1: cria a baseline e guarda no estado do card.
  async function criarBaseline() {
    setErro("");
    setDiff(null);
    setBaseline(null);
    if (pasta.length === 0) {
      setErro("Informe o caminho de uma pasta.");
      return;
    }
    try {
      const resp = await fetch(`${API}/api/integrity/baseline`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pasta: pasta }),
      });
      const dados = await resp.json();
      if (dados.erro) {           // a API avisou que a pasta nao existe
        setErro(dados.erro);
        return;
      }
      setBaseline(dados.baseline);
      setTotal(dados.total);
    } catch (e) {
      setErro("Nao consegui falar com a API (porta 8000).");
    }
  }

  // Passo 2: manda a pasta + a baseline guardada e recebe o diff.
  async function verificar() {
    setErro("");
    setDiff(null);
    try {
      const resp = await fetch(`${API}/api/integrity/verify`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pasta: pasta, baseline: baseline }),
      });
      const dados = await resp.json();
      if (dados.erro) {
        setErro(dados.erro);
        return;
      }
      setDiff(dados);
    } catch (e) {
      setErro("Nao consegui falar com a API (porta 8000).");
    }
  }

  // Quantas mudancas no total? (usado pra mostrar "tudo integro").
  const totalMudancas = diff
    ? diff.modificados.length + diff.adicionados.length + diff.removidos.length
    : 0;

  return (
    <div className="card">
      <div className="card-head" onClick={() => setAberto(!aberto)}>
        <span className="card-icon">🔎</span>
        <div>
          <h3 className="card-title">File Integrity Checker</h3>
          <p className="card-desc">Detecta arquivos alterados, criados ou removidos</p>
        </div>
        <span className={aberto ? "card-arrow open" : "card-arrow"}>▶</span>
      </div>

      {aberto && (
        <div className="card-body">
          <label className="field-label">Caminho da pasta</label>
          <input
            className="text-input"
            placeholder={PASTA_EXEMPLO}
            value={pasta}
            onChange={(e) => setPasta(e.target.value)}
          />

          <button className="btn" onClick={criarBaseline}>
            1 · Criar Baseline (tirar a foto)
          </button>

          {/* So mostra o botao de verificar DEPOIS que existe uma baseline.
              disabled continua barrando ate a foto existir. */}
          <button
            className="btn"
            onClick={verificar}
            disabled={!baseline}
            style={{ background: "var(--accent-2)", color: "#04121f" }}
          >
            2 · Verificar Integridade
          </button>

          {erro && <p className="error">{erro}</p>}

          {baseline && (
            <p className="fi-status">
              📸 Baseline criada: <b>{total}</b> arquivo(s) protegido(s).
            </p>
          )}

          {/* Resultado da verificacao */}
          {diff && (
            <div className="fi-result">
              {totalMudancas === 0 ? (
                <p className="fi-ok">✓ Tudo integro — nenhuma mudanca detectada.</p>
              ) : (
                <>
                  <ListaMudanca titulo="Modificados" itens={diff.modificados} cor="#f0883e" />
                  <ListaMudanca titulo="Adicionados" itens={diff.adicionados} cor="#58a6ff" />
                  <ListaMudanca titulo="Removidos"   itens={diff.removidos}   cor="#f85149" />
                </>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// Pequeno componente auxiliar: mostra uma categoria de mudanca.
// So aparece se tiver pelo menos 1 item. Repare que da pra criar
// componentes menores pra organizar -- boa pratica no React.
function ListaMudanca({ titulo, itens, cor }) {
  if (itens.length === 0) return null;
  return (
    <div className="fi-grupo">
      <div className="fi-grupo-titulo" style={{ color: cor }}>
        {titulo} ({itens.length})
      </div>
      <ul>
        {itens.map((nome) => (
          <li key={nome}>{nome}</li>
        ))}
      </ul>
    </div>
  );
}
