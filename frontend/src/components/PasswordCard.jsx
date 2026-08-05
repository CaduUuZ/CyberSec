// ============================================================
//  CARD 2 - Password Strength Checker (frontend)
//  Card expansivel com barra de forca colorida e criterios.
// ============================================================

import { useState } from "react";

const API = "http://127.0.0.1:8000";

// Uma cor para cada nota de 1 a 5 (vermelho -> verde).
// O indice 0 fica cinza (estado "vazio"). Assim CORES[nota] ja
// devolve a cor certa direto pela nota.
const CORES = ["#30363d", "#f85149", "#f0883e", "#e3b341", "#3fb950", "#2ecc71"];

// Rotulos amigaveis para cada criterio (chave da API -> texto na tela).
const LABELS_CRITERIOS = {
  tamanho_8: "8+ caracteres",
  minuscula: "Letra minuscula",
  maiuscula: "Letra maiuscula",
  numero: "Numero",
  simbolo: "Simbolo",
};

export default function PasswordCard() {
  const [aberto, setAberto] = useState(false);
  const [senha, setSenha] = useState("");
  const [analise, setAnalise] = useState(null); // resultado da API
  const [erro, setErro] = useState("");

  async function analisar() {
    setErro("");
    if (senha.length === 0) {
      setAnalise(null);
      setErro("Digite uma senha primeiro.");
      return;
    }
    try {
      const resposta = await fetch(`${API}/api/password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ senha: senha }),
      });
      const dados = await resposta.json();
      setAnalise(dados);
    } catch (e) {
      setErro("Nao consegui falar com a API (porta 8000 esta rodando?).");
    }
  }

  return (
    <div className="card">
      <div className="card-head" onClick={() => setAberto(!aberto)}>
        <span className="card-icon">🛡️</span>
        <div>
          <h3 className="card-title">Password Strength Checker</h3>
          <p className="card-desc">Mede a forca e a entropia da senha</p>
        </div>
        <span className={aberto ? "card-arrow open" : "card-arrow"}>▶</span>
      </div>

      {aberto && (
        <div className="card-body">
          <label className="field-label">Senha para analisar</label>
          <input
            className="text-input"
            placeholder="ex: Banana123!"
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && analisar()}
          />
          <button className="btn" onClick={analisar}>Analisar</button>

          {erro && <p className="error">{erro}</p>}

          {/* Se ja temos analise, mostramos barra + criterios + entropia. */}
          {analise && (
            <div className="pw-result">
              {/* Barra de 5 segmentos. Criamos um array [0,1,2,3,4] com
                  [...Array(5).keys()] e desenhamos um bloco pra cada.
                  O bloco "acende" (ganha cor) se seu indice < nota. */}
              <div className="pw-bar">
                {[...Array(5).keys()].map((i) => (
                  <div
                    key={i}
                    className="pw-seg"
                    // 'style' inline: aqui a cor depende do resultado,
                    // entao nao da pra fixar no CSS -> definimos aqui.
                    style={{
                      background: i < analise.nota ? CORES[analise.nota] : CORES[0],
                    }}
                  />
                ))}
              </div>

              <div className="pw-label" style={{ color: CORES[analise.nota] }}>
                {analise.rotulo} · {analise.entropia_bits} bits de entropia
              </div>

              {/* Lista de criterios com check verde ou x cinza. */}
              <ul className="pw-criterios">
                {Object.entries(analise.criterios).map(([chave, ok]) => (
                  <li key={chave} className={ok ? "ok" : "no"}>
                    {ok ? "✓" : "✗"} {LABELS_CRITERIOS[chave] || chave}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
