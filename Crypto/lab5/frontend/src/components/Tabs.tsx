import { useState } from "react";
import type { EndpointConfig } from "../config/apiConfig";

export function Tabs({
  tabs,
  render,
}: {
  tabs: EndpointConfig[];
  render: (tab: EndpointConfig) => React.ReactNode;
}) {
  const [active, setActive] = useState(0);

  return (
    <div className="w-full">
      <div className="flex flex-wrap gap-2 border-b border-border pb-2">
        {tabs.map((t, i) => (
          <button
            key={t.key}
            onClick={() => setActive(i)}
            className={`
              px-4 py-2 rounded-lg transition-all duration-200
              text-sm font-medium
              ${
                active === i
                  ? "bg-surface text-blue shadow-neonBlue"
                  : "bg-surface2 text-muted hover:text-text hover:bg-surface"
              }
            `}
          >
            {t.label}
          </button>
        ))}
      </div>

      <div className="mt-4" key={tabs[active].key}>
        {render(tabs[active])}
      </div>
    </div>
  );
}