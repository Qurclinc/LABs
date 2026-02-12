interface Props {
  value: string;
  onChange: (v: string) => void;
  onGenerate: () => void;
}

function KeyInput({ value, onChange, onGenerate }: Props) {
  return (
    <div className="flex gap-2">
      <input
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Key"
        className="flex-1 bg-surfaceDark border border-purple rounded px-3 py-2 text-text"
      />
      <button
        onClick={onGenerate}
        className="bg-purple text-black px-3 rounded hover:opacity-80"
      >
        Auto
      </button>
    </div>
  );
}

export default KeyInput;
