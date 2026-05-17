export function EEATable({ data }: { data: number[][] }) {
  // Находим НОД (последнее ненулевое a)
  const gcd = data[data.length - 1]?.[0] ?? 0;
  
  // Берём коэффициенты из последней строки (x и y)
  const lastRow = data[data.length - 1];
  const x = lastRow?.[1] ?? 0;
  const y = lastRow?.[2] ?? 0;
  
  // a и b из первой строки (исходные числа)
  const a0 = data[0]?.[0] ?? 0;
  const b0 = data[1]?.[0] ?? 0;

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm border border-border rounded-xl overflow-hidden">
        <thead className="bg-surface2 text-muted">
          <tr>
            <th className="p-2">i</th>
            <th className="p-2">a</th>
            <th className="p-2">x</th>
            <th className="p-2">y</th>
            <th className="p-2">q</th>
          </tr>
        </thead>

        <tbody>
          {data.map((row, i) => {
            const [a, xVal, yVal, q] = row;

            return (
              <tr
                key={i}
                className="
                  text-center border-t border-border
                  hover:bg-surface2 transition
                "
              >
                <td className="p-2 text-muted">{i}</td>

                <td className="p-2 text-blue font-semibold">{a}</td>

                <td className="p-2">{xVal ?? "-"}</td>
                <td className="p-2">{yVal ?? "-"}</td>

                <td className="p-2 text-yellow">
                  {q !== undefined ? q : "-"}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>

      {/* Линейное разложение */}
      <div className="mt-4 p-3 bg-surface2 rounded-lg text-center text-green font-mono text-lg">
        {a0} · ({x}) + {b0} · ({y}) = {gcd}
      </div>
    </div>
  );
}