// ============================================================
//  CARD 5 - Log Analyzer (frontend)
//  Cola um log de autenticacao e recebe um relatorio de seguranca.
// ============================================================

import { useState } from "react";

const API = "http://127.0.0.1:8000";

// Log de exemplo ja preenchido, pra facilitar o teste.
const LOG_EXEMPLO = `Aug  5 03:11:01 srv sshd[2001]: Failed password for admin from 203.0.113.77 port 51512 ssh2
Aug  5 03:11:03 srv sshd[2002]: Failed password for admin from 203.0.113.77 port 51513 ssh2
Aug  5 03:11:05 srv sshd[2003]: Failed password for root from 203.0.113.77 port 51514 ssh2
Aug  5 03:11:07 srv sshd[2004]: Failed password for root from 203.0.113.77 port 51515 ssh2
Aug  5 03:11:09 srv sshd[2005]: Failed password for admin from 203.0.113.77 port 51516 ssh2
Aug  5 03:11:11 srv sshd[2006]: Failed password for oracle from 203.0.113.77 port 51517 ssh2
Aug  5 03:11:13 srv sshd[2007]: Failed password for postgres from 203.0.113.77 port 51518 ssh2
Aug  5 03:11:15 srv sshd[2008]: Failed password for admin from 203.0.113.77 port 51519 ssh2
Aug  5 09:02:44 srv sshd[3100]: Accepted password for cadu from 192.168.0.10 port 40122 ssh2
Aug  5 14:41:08 srv sshd[3300]: Failed password for admin from 198.51.100.23 port 33210 ssh2
Aug  5 14:41:30 srv sshd[3301]: Failed password for admin from 198.51.100.23 port 33222 ssh2
Aug  5 22:58:12 srv sshd[3990]: Accepted password for cadu from 192.168.0.10 port 41999 ssh2`;

export default function LogAnalyzerCard() {
  const [aberto, setAberto] = useState(false);
  const [texto, setTexto] = useState(LOG_EXEMPLO);
  const [rel, setRel] = useState(null);   // relatorio da API
  const [erro, setErro] = useState("");

  async function analisar() {
    setErro("");
    setRel(null);
    if (texto.trim().length === 0) {
      setErro("Cole o conteudo de um log primeiro.");
      return;
    }
    try {
      const resp = await fetch(`${API}/api/logs`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ texto: texto }),
      });
      setRel(await resp.json());
    } catch (e) {
      setErro("Nao consegui falar com a API (porta 8000).");
    }
  }

  // Maior valor das horas, pra escalar as barras do grafico.
  const maxHora = rel
    ? Math.max(1, ...Object.values(rel.falhas_por_hora))
    : 1;

  return (
    <div className="card">
      <div className="card-head" onClick={() => setAberto(!aberto)}>
        <span className="card-icon">📊</span>
        <div>
          <h3 className="card-title">Log Analyzer</h3>
          <p className="card-desc">Detecta forca bruta e IPs suspeitos em logs</p>
        </div>
        <span className={aberto ? "card-arrow open" : "card-arrow"}>▶</span>
      </div>

      {aberto && (
        <div className="card-body">
          <label className="field-label">Cole o log de autenticacao (formato SSH/auth.log)</label>
          <textarea
            className="text-input log-area"
            rows={6}
            value={texto}
            onChange={(e) => setTexto(e.target.value)}
          />
          <button className="btn" onClick={analisar}>Analisar Log</button>

          {erro && <p className="error">{erro}</p>}

          {rel && (
            <div className="log-result">
              {/* Alertas de forca bruta no topo, se houver. */}
              {rel.suspeitos.length > 0 && (
                <div className="log-alertas">
                  {rel.suspeitos.map((s) => (
                    <div key={s.ip} className="log-alerta">
                      🚨 <b>{s.ip}</b> — {s.falhas} falhas (possivel forca bruta)
                    </div>
                  ))}
                </div>
              )}

              {/* Numeros gerais */}
              <div className="log-stats">
                <div><span>{rel.total_linhas}</span>linhas</div>
                <div><span className="c-red">{rel.total_falhas}</span>falhas</div>
                <div><span className="c-green">{rel.total_sucessos}</span>sucessos</div>
              </div>

              {/* Falhas por IP */}
              <div className="log-bloco">
                <div className="log-bloco-titulo">Falhas por IP</div>
                {rel.falhas_por_ip.map((item) => (
                  <div key={item.ip} className="log-linha">
                    <span className="mono">{item.ip}</span>
                    <span>{item.falhas}</span>
                  </div>
                ))}
              </div>

              {/* Usuarios mais tentados */}
              <div className="log-bloco">
                <div className="log-bloco-titulo">Usuarios mais tentados</div>
                {rel.usuarios_mais_tentados.map((item) => (
                  <div key={item.usuario} className="log-linha">
                    <span className="mono">{item.usuario}</span>
                    <span>{item.tentativas}</span>
                  </div>
                ))}
              </div>

              {/* Mini grafico de falhas por hora */}
              <div className="log-bloco">
                <div className="log-bloco-titulo">Falhas por hora</div>
                <div className="log-chart">
                  {Object.entries(rel.falhas_por_hora)
                    .sort()   // ordena pelas horas
                    .map(([hora, qtd]) => (
                      <div key={hora} className="log-bar-col">
                        <div
                          className="log-bar"
                          style={{ height: `${(qtd / maxHora) * 60}px` }}
                          title={`${qtd} falhas`}
                        />
                        <span className="log-hora">{hora}h</span>
                      </div>
                    ))}
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
