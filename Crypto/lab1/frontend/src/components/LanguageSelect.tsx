interface Props {
  value: string;
  onChange: (v: string) => void;
}

function LanguageSelect({ value, onChange }: Props) {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="bg-surfaceDark border border-cyan text-text rounded px-3 py-2"
    >
      <option value="eng">eng</option>
      <option value="rus">rus</option>
    </select>
  );
}

export default LanguageSelect;
