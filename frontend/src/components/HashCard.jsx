// ============================================================
//  CARD 1 - Hash Generator (frontend)
//  Um card expansivel que chama a API Python e mostra os hashes.
// ============================================================

// 'useState' e a ferramenta do React pra dar "memoria" ao componente.
import { useState } from "react";

// Endereco da nossa API (o servidor FastAPI que ja esta rodando).
const API = "http://127.0.0.1:8000";

// Um componente e uma funcao que devolve JSX (o "HTML" do React).
export default function HashCard() {
  // ---- Estados (a memoria do card) ----
  // Cada useState devolve: [valor atual, funcao pra mudar o valor].
  const [aberto, setAberto] = useState(false);   // card expandido ou nao
  const [texto, setTexto] = useState("");         // o que o usuario digitou
  const [hashes, setHashes] = useState(null);     // resultado vindo da API
  const [erro, setErro] = useState("");           // mensagem de erro
  const [carregando, setCarregando] = useState(false); // esperando a API?

  // ---- Funcao que chama a API ----
  // 'async' permite usar 'await' (esperar a resposta da internet).
  async function gerarHash() {
    setErro("");
    setHashes(null);

    if (texto.length === 0) {
      setErro("Digite algum texto primeiro.");
      return;
    }

    setCarregando(true);
    try {
      // fetch = faz a chamada HTTP pra nossa API.
      const resposta = await fetch(`${API}/api/hash`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        // O corpo precisa ser texto JSON -> JSON.stringify converte.
        body: JSON.stringify({ texto: texto }),
      });

      // Converte a resposta (JSON) num objeto JavaScript.
      const dados = await resposta.json();

      // Guarda os hashes no estado -> o React redesenha a tela sozinho.
      setHashes(dados.hashes);
    } catch (e) {
      setErro("Nao consegui falar com a API. Ela esta rodando na porta 8000?");
    } finally {
      setCarregando(false);
    }
  }

  // ---- O que aparece na tela (JSX) ----
  return (
    <div className="card">
      {/* Cabecalho: clicar abre/fecha o card (inverte 'aberto'). */}
      <div className="card-head" onClick={() => setAberto(!aberto)}>
        <span className="card-icon">🔐</span>
        <div>
          <h3 className="card-title">Hash Generator</h3>
          <p className="card-desc">Gera MD5, SHA-1, SHA-256 e SHA-512</p>
        </div>
        <span className={aberto ? "card-arrow open" : "card-arrow"}>▶</span>
      </div>

      {/* So mostra o corpo se 'aberto' for true.
          O '&&' e um atalho: "se aberto, entao renderiza isto". */}
      {aberto && (
        <div className="card-body">
          <label className="field-label">Texto para gerar o hash</label>
          <input
            className="text-input"
            placeholder="ex: senha123"
            value={texto}
            // Toda vez que o usuario digita, atualizamos o estado 'texto'.
            onChange={(e) => setTexto(e.target.value)}
            // Enter tambem dispara o hash.
            onKeyDown={(e) => e.key === "Enter" && gerarHash()}
          />

          <button className="btn" onClick={gerarHash} disabled={carregando}>
            {carregando ? "Gerando..." : "Gerar Hash"}
          </button>

          {erro && <p className="error">{erro}</p>}

          {/* Se ja temos hashes, mostramos cada um.
              Object.entries transforma o dicionario numa lista de
              pares [algoritmo, valor] pra podermos percorrer com .map. */}
          {hashes && (
            <div className="result">
              {Object.entries(hashes).map(([algo, valor]) => (
                <div className="hash-row" key={algo}>
                  <div className="hash-algo">{algo}</div>
                  <div className="hash-value">{valor}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
