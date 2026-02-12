export type CipherType = "shift" | "substitution" | "vigenere";
export type Mode = "encrypt" | "decrypt";

export interface CipherRequest {
    mode: Mode;
    plain_text: string;
    lang: string;
    key: string | number;
    length?: number;
}

export interface CipherResponse {
    cipher_text?: string;
    plain_text?: string;
    key?: string | number;
}
