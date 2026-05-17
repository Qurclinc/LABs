import { useState, useRef, useEffect } from "react";
import { post } from "../services/api";
import { Loader } from "./Loader";
import { EEATable } from "./EEATable";
import { cancellable } from "../config/apiConfig";
import type { EndpointConfig, FieldConfig } from "../config/apiConfig";

function parseList(input: string): number[] {
  return input
    .split(/[\s,]+/)
    .map((x) => x.trim())
    .filter(Boolean)
    .map(Number)
    .filter((x) => !isNaN(x));
}

function parseValue(field: FieldConfig, value: string) {
  switch (field.type) {
    case "int":
      return Number(value);

    case "list":
      const parsed = parseList(value);
      if (!parsed.length) throw new Error("Введите список чисел");
      return parsed;

    case "bool":
      return Boolean(value);

    default:
      return String(value);
  }
}

export function Form({ config }: { config: EndpointConfig }) {
  const [values, setValues] = useState<Record<string, string>>({});
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const controllerRef = useRef<AbortController | null>(null);

  const handleChange = (k: string, v: any) => {
    setValues((p) => ({ ...p, [k]: v }));
  };

  const handleSubmit = async () => {
    if (!config.endpoint) return;

    controllerRef.current?.abort();

    const controller = new AbortController();
    controllerRef.current = controller;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const payload: any = {};

      for (const field of config.fields) {
        payload[field.name] = parseValue(field, values[field.name] || "");
      }

      let res = await post(config.endpoint, payload, controller.signal);

      if (typeof res === "boolean") {
        res = res ? "Простое" : "Составное";
      }

      setResult(res);
    } catch (e: any) {
      if (e.name !== "AbortError") {
        setError(e.message);
      }
    } finally {
      setLoading(false);
    }
  };

  const cancel = () => controllerRef.current?.abort();

  useEffect(() => {
    return () => controllerRef.current?.abort();
  }, []);

  return (
    <div className="bg-surface rounded-2xl p-6 shadow-lg border border-border max-w-3xl">
      <h2 className="text-xl mb-4 text-blue font-semibold">
        {config.label}
      </h2>

      <div className="flex flex-col gap-3">
        {config.fields.map((f) =>
          f.type === "bool" ? (
            <label key={f.name} className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={Boolean(values[f.name])}
                onChange={(e) => handleChange(f.name, e.target.checked)}
              />
              {f.name}
            </label>
          ) : (
            <input
              key={f.name}
              value={values[f.name] || ""}
              onChange={(e) => handleChange(f.name, e.target.value)}
              placeholder={f.placeholder || f.name}
              disabled={loading}
              className="bg-surface2 border border-border rounded-lg p-2 text-text"
            />
          )
        )}

        <div className="flex gap-2">
          <button
            onClick={handleSubmit}
            disabled={loading}
            className="flex-1 bg-blue text-bg font-semibold py-2 rounded-lg"
          >
            {loading ? "Вычисление..." : "Вычислить"}
          </button>

          {loading && cancellable.includes(config.key) && (
            <button onClick={cancel} className="px-3 bg-red rounded-lg">
              ✕
            </button>
          )}
        </div>
      </div>

      {loading && <Loader />}

      {error && (
        <div className="mt-4 bg-red/20 border border-red text-red p-3 rounded-lg">
          {error}
        </div>
      )}

      {result !== null && (
        <div className="mt-4 bg-surface2 p-3 rounded-lg text-green">
          {config.key === "primitiveroot" && Array.isArray(result) ? (
            <div className="flex flex-wrap gap-2">
              {result.map((x: string, i: number) => (
                <span key={i} className="px-2 py-1 bg-bg rounded">
                  {x}
                </span>
              ))}
            </div>
          ) : config.key === "eea" ? (
            <EEATable data={result} />
          ) : config.key === "single" && Array.isArray(result) ? (
            result.map((x: string, i: number) => (
              <div key={i}>x ≡ {x} (mod {values["m"]})</div>
            ))
          ) : (
            <pre>{JSON.stringify(result, null, 2)}</pre>
          )}
        </div>
      )}
    </div>
  );
}