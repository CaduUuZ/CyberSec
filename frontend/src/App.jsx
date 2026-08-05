// ============================================================
//  App principal - CyberSec Toolkit
//  Monta o cabecalho e a grade de cards.
// ============================================================

import HashCard from "./components/HashCard";
import PasswordCard from "./components/PasswordCard";
import FileIntegrityCard from "./components/FileIntegrityCard";
import ScannerCard from "./components/ScannerCard";

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

        {/* Card 3 - pronto! */}
        <FileIntegrityCard />

        {/* Card 4 - pronto! */}
        <ScannerCard />

        {/* Os proximos cards entram aqui:
            ...cada feature nova = um componente nesta grade. */}
      </main>
    </>
  );
}
