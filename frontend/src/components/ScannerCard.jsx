// ============================================================
//  CARD 4 - Port Scanner (frontend)
//  Escaneia uma faixa de portas de um host e lista as abertas.
//  ETICA: use apenas em sistemas seus ou com autorizacao.
// ============================================================

import { useState } from "react";

const API = "http://127.0.0.1:8000";

export default function ScannerCard() {
  const [aberto, setAberto] = useState(false);
  const [host, setHost] = useState("127.0.0.1");
  const [inicio, setInicio] = useState(1);
  const [fim, setFim] = useState(1024);
  const [resultado, setResultado] = useState(null);
  const [erro, setErro] = useState("");
  const [carregando, setCarregando] = useState(false);

  async function escanear() {
    setErro("");
    setResultado(null);
    setCarregando(true);
    try {
      const resp = await fetch(`${API}/api/scan`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        // Number(...) garante que enviamos numeros, nao texto.
        body: JSON.stringify({
          host: host,
          inicio: Number(inicio),
          fim: Number(fim),
        }),
      });
      const dados = await resp.json();
      if (dados.erro) {
        setErro(dados.erro);
        return;
      }
      setResultado(dados);
    } catch (e) {
      setErro("Nao consegui falar com a API (porta 8000).");
    } finally {
      setCarregando(false);
    }
  }

  return (
    <div className="card">
      <div className="card-head" onClick={() => setAberto(!aberto)}>
        <span className="card-icon">📡</span>
        <div>
          <h3 className="card-title">Port Scanner</h3>
          <p className="card-desc">Descobre portas abertas e seus servicos</p>
        </div>
        <span className={aberto ? "card-arrow open" : "card-arrow"}>▶</span>
      </div>

      {aberto && (
        <div className="card-body">
          {/* Aviso etico sempre visivel dentro do card. */}
          <p className="aviso">
            ⚠️ Escaneie apenas sistemas seus ou com autorizacao.
          </p>

          <label className="field-label">Host / IP</label>
          <input
            className="text-input"
            value={host}
            onChange={(e) => setHost(e.target.value)}
          />

          {/* Dois campos numericos lado a lado (faixa de portas). */}
          <div className="scan-faixa">
            <div>
              <label className="field-label">Porta inicial</label>
              <input
                className="text-input"
                type="number"
                value={inicio}
                onChange={(e) => setInicio(e.target.value)}
              />
            </div>
            <div>
              <label className="field-label">Porta final</label>
              <input
                className="text-input"
                type="number"
                value={fim}
                onChange={(e) => setFim(e.target.value)}
              />
            </div>
          </div>

          <button className="btn" onClick={escanear} disabled={carregando}>
            {carregando ? "Escaneando..." : "Escanear"}
          </button>

          {erro && <p className="error">{erro}</p>}

          {resultado && (
            <div className="scan-result">
              <p className="scan-info">
                {resultado.host} ({resultado.ip}) · portas {resultado.faixa} ·{" "}
                {resultado.segundos}s
              </p>

              {resultado.abertas.length === 0 ? (
                <p className="fi-ok">Nenhuma porta aberta nessa faixa.</p>
              ) : (
                <table className="scan-tabela">
                  <thead>
                    <tr>
                      <th>Porta</th>
                      <th>Servico</th>
                    </tr>
                  </thead>
                  <tbody>
                    {resultado.abertas.map((p) => (
                      <tr key={p.porta}>
                        <td className="scan-porta">{p.porta}</td>
                        <td>{p.servico}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
