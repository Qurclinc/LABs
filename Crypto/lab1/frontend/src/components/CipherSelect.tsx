import type { CipherType } from "../types/ciphers";

interface Props {
    value: CipherType;
    onChange: (v: CipherType) => void;
}

function CipherSelect({ value, onChange }: Props) {
    return (
        <select
        value={value}
        onChange={(e) => onChange(e.target.value as CipherType)}
        className="bg-surfaceDark border border-cyan text-text rounded px-3 py-2"
        >

        <option value="shift">Shift</option>
        <option value="substitution">Substitution</option>
        <option value="vigenere">Vigenere</option>
        </select>
    );
}

export default CipherSelect;
