// ============================================================
//  App principal - CyberSec Toolkit
//  Monta o cabecalho e a grade de cards.
// ============================================================

import HashCard from "./components/HashCard";
import PasswordCard from "./components/PasswordCard";

export default function App() {
  return (
    <>
      <header className="header">
        <h1>
          <span className="accent">Cyber</span>Sec Toolkit
        </h1>
        <p>Ferramentas de seguranca — um card por vez 🛡️</p>
      </header>

      <main className="grid">
        {/* Card 1 - pronto! */}
        <HashCard />

        {/* Card 2 - pronto! */}
        <PasswordCard />

        {/* Os proximos cards entram aqui:
            <FileIntegrityCard />
            ...cada feature nova = um componente nesta grade. */}
      </main>
    </>
  );
}
