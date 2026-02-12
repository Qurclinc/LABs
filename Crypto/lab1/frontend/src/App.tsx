import { useState } from "react";
import Header from "./components/Header";
import CipherSelect from "./components/CipherSelect";
import CipherPanel from "./components/CipherPanel";
import LanguageSelect from "./components/LanguageSelect";
import type { CipherType } from "./types/ciphers";

function App() {
  const [cipher, setCipher] = useState<CipherType>("shift");
  const [lang, setLang] = useState("eng");

  return (
    <>
      <Header />

      <main className="max-w-screen-xl mx-auto px-6 py-10">
        <div className="mb-6 flex items-center gap-6">
          <div className="flex items-center gap-2">
            <span className="text-muted">Algorithm:</span>
            <CipherSelect value={cipher} onChange={setCipher} />
          </div>

          <div className="flex items-center gap-2">
            <span className="text-muted">Language:</span>
            <LanguageSelect value={lang} onChange={setLang} />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-6">
          <CipherPanel mode="encrypt" cipher={cipher} lang={lang} />
          <CipherPanel mode="decrypt" cipher={cipher} lang={lang} />
        </div>
      </main>
    </>
  );
}

export default App;
