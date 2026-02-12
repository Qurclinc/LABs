import { useState } from "react";
import type { CipherType, Mode } from "../types/ciphers";
import { processCipher } from "../services/api";
import KeyInput from "./KeyInput";

interface Props {
  mode: Mode;
  cipher: CipherType;
  lang: string;
}

function CipherPanel({ mode, cipher, lang }: Props) {
  const [text, setText] = useState("");
  const [result, setResult] = useState("");
  const [key, setKey] = useState("");
  const [generatedKey, setGeneratedKey] = useState<string | number | null>(null);
  const [length, setLength] = useState<number | "">("");
  const [error, setError] = useState<string | null>(null);

  const isKeyValid = key.trim() !== "";

  async function handleSubmit() {
    if (!isKeyValid) return;

    setError(null);

    try {
      const payload: any = {
        mode,
        plain_text: text,
        lang,
        key: key,
      };

      const parsedKey =
        cipher === "shift" ? Number(key) : key;

      payload.key = key === "-1" ? -1 : parsedKey;

      if (cipher === "vigenere") {
        payload.length = length ? length : 0;
      }

      const res = await processCipher(cipher, payload);

      if (res.key !== undefined) {
        setGeneratedKey(res.key);
        setKey(String(res.key));
      }

      setResult(res.cipher_text || res.plain_text || "");
    } catch {
      setError("Ошибка обработки запроса (проверь ключ / формат данных)");
    }
  }

  return (
    <div className="flex flex-col gap-3 w-full p-4 rounded border border-cyan bg-surfaceDark">
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder={mode === "encrypt" ? "Plain text" : "Cipher text"}
        className="h-40 resize-none bg-surface border border-cyan rounded p-3 text-text"
      />

      <KeyInput
        value={key}
        onChange={setKey}
        onGenerate={() => setKey("-1")}
      />

      {cipher === "vigenere" && (
        <input
          type="number"
          placeholder="Key length (optional)"
          value={length}
          onChange={(e) =>
            setLength(e.target.value ? Number(e.target.value) : "")
          }
          className="bg-surface border border-purple rounded px-3 py-2 text-text"
        />
      )}

      {generatedKey !== null && (
        <div className="text-sm text-secondary">
          Generated key: <span className="text-text">{generatedKey}</span>
        </div>
      )}

      {error && (
        <div className="text-sm text-error border border-error p-2 rounded">
          {error}
        </div>
      )}

      <button
        disabled={!isKeyValid}
        onClick={handleSubmit}
        className={`mt-2 py-2 rounded font-semibold transition
          ${
            mode === "encrypt"
              ? "bg-primary text-black shadow-neonBlue"
              : "bg-accent text-black shadow-neonPink"
          }
          ${
            !isKeyValid
              ? "opacity-40 cursor-not-allowed shadow-none"
              : "hover:opacity-90"
          }
        `}
      >
        {mode === "encrypt" ? "Encrypt" : "Decrypt"}
      </button>

      <textarea
        value={result}
        readOnly
        placeholder="Result"
        className="h-40 resize-none bg-surface border border-purple rounded p-3 text-text"
      />
    </div>
  );
}

export default CipherPanel;
