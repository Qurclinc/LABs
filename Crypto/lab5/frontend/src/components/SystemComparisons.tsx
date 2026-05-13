import { useState } from "react";
import { post } from "../services/api";

export function SystemComparisons() {
  const [rows, setRows] = useState([["1", "0", "1"]]);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const update = (i: number, j: number, val: string) => {
    const copy = [...rows];
    copy[i][j] = val;
    setRows(copy);
  };

  const addRow = () => setRows([...rows, ["1", "0", "1"]]);

  const send = async () => {
    try {
      setError(null);
      const res = await post("/api/comparision/system", {
        coeffs: rows,
      });
      setResult(res);
    } catch (e: any) {
      setResult(null);
      setError(e.message);
    }
  };

  return (
    <div className="bg-surface p-6 rounded-2xl border border-border max-w-3xl">
      <h2 className="text-xl text-purple mb-4">Система сравнений</h2>

      <div className="flex flex-col gap-3">
        {rows.map((_, i) => (
          <div key={i} className="flex gap-2">
            <input
              placeholder="a"
              className="flex-1 bg-surface2 border border-border p-2 rounded-lg"
              onChange={(e) => update(i, 0, e.target.value)}
            />
            <input
              placeholder="b"
              className="flex-1 bg-surface2 border border-border p-2 rounded-lg"
              onChange={(e) => update(i, 1, e.target.value)}
            />
            <input
              placeholder="m"
              className="flex-1 bg-surface2 border border-border p-2 rounded-lg"
              onChange={(e) => update(i, 2, e.target.value)}
            />
          </div>
        ))}

        <div className="flex gap-2 mt-2">
          <button
            onClick={addRow}
            className="px-3 py-2 bg-magenta rounded-lg hover:shadow-neonPurple"
          >
            +
          </button>

          <button
            onClick={send}
            className="flex-1 bg-green text-bg rounded-lg py-2 hover:shadow-neonGreen"
          >
            Решить
          </button>
        </div>
      </div>

      {error && (
        <div className="mt-4 bg-red/20 border border-red text-red p-3 rounded-lg">
          {error}
        </div>
      )}

      {result && (
        <pre className="mt-4 bg-surface2 p-3 rounded-lg text-green">
          {/* {JSON.stringify(result, null, 2)} */}
          x ≡ {result["X"]} (mod {result["M"]}) 
        </pre>
      )}
    </div>
  );
}