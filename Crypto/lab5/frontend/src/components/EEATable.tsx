export function EEATable({ data }: { data: number[][] }) {
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
            const [a, x, y, q] = row;

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

                <td className="p-2">{x ?? "-"}</td>
                <td className="p-2">{y ?? "-"}</td>

                <td className="p-2 text-yellow">
                  {q !== undefined ? q : "-"}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}