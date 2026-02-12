import type { CipherRequest, CipherResponse, CipherType } from "../types/ciphers";

const BASE_URL = "/api/historical";

export async function processCipher(
    type: CipherType,
    payload: CipherRequest
): Promise<CipherResponse> {
    const endpoint = {
        shift: "shift",
        substitution: "substitution",
        vigenere: "vigenere",
    }[type];

    const res = await fetch(`${BASE_URL}/${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    });

    if (!res.ok) {
        throw new Error("Request failed");
    }

    return res.json();
}
