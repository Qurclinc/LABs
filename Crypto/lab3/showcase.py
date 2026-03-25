import numpy as np
import pandas as pd

def E(data):
    return -sum(p * np.log2(p) for p in data if p > 1e-12)

def do_report(
    filename: str,
    cipher_matrix,
    p_c_m,
    p_m_c,
    h_m, h_k, h_c,
    info_leakage,
    p_k,
    p_m,
    p_c,
    alphabet
):
    s = len(alphabet)
    n = len(p_k)
    
    with open(filename, "w", encoding="UTF-8") as f:
        f.write("1. МАТРИЦА ШИФРОВАНИЯ Ek:\n")
        df_ek = pd.DataFrame(cipher_matrix, columns=alphabet, index=[f"k{j+1}" for j in range(n)])
        f.write(df_ek.to_string())
        f.write("\n\n")
        
        f.write("2. ВЕРОЯТНОСТИ ШИФРТЕКСТА ПРИ ДАННОМ ОТКРЫТОМ ТЕКСТЕ P(c|m):\n")
        df_pcm = pd.DataFrame(p_c_m, index=alphabet, columns=[f"{x}" for x in range(1, s+1)])
        f.write(df_pcm.round(4).to_string())
        f.write("\n\n")
        
        f.write("3. ВЕРОЯТНОСТИ ОТКРЫТОГО ТЕКСТА ПРИ ДАННОМ ШИФРТЕКСТЕ P(m|c):\n")
        df_pmc = pd.DataFrame(p_m_c, index=alphabet, columns=[f"{x}" for x in range(1, s+1)])
        f.write(df_pmc.round(4).to_string())
        f.write("\n\n")
        
        f.write("4. ЭНТРОПИИ И УТЕЧКА:\n")
        f.write(f"H(M) Сообщения:   {h_m:.4f} бит\n")
        f.write(f"H(K) Ключи:       {h_k:.4f} бит\n")
        f.write(f"H(C) Шифртекст:   {h_c:.4f} бит\n")
        f.write(f"I(M; C) УТЕЧКА:   {max(0, info_leakage):.4f} бит\n\n")
        
        f.write("5. РАСПРЕДЕЛЕНИЕ ВЕРОЯТНОСТЕЙ ОТКРЫТОГО ТЕКСТА P(m):\n")
        msg_probs = " | ".join([f"{alphabet[j]}: {p_m[j]:.4f}" for j in range(len(p_m))])
        f.write(msg_probs + "\n\n")
        
        f.write("6. РАСПРЕДЕЛЕНИЕ ВЕРОЯТНОСТЕЙ КЛЮЧЕЙ P(k):\n")
        key_probs = " | ".join([f"k{j+1}: {p_k[j]:.4f}" for j in range(len(p_k))])
        f.write(key_probs + "\n\n")
        
        f.write("7. РАСПРЕДЕЛЕНИЕ ВЕРОЯТНОСТЕЙ ШИФРТЕКСТА P(c):\n")
        f.write(f"{p_c.round(4)}\n\n")


def main():
    alphabet = list("ABCD")
    len_alphabet = len(alphabet)
    keys_amount = 3
    
    # Table Ek
    ciphertexts = []
    ciphertexts.append(np.array([3, 4, 2, 1]))
    ciphertexts.append(np.array([3, 1, 4, 2]))
    ciphertexts.append(np.array([4, 3, 1, 2]))
    
    p_m = np.array([0.25, 0.3, 0.15, 0.3])
    p_k = np.array([0.25, 0.5, 0.25])
    
    # p(c)
    p_c = np.zeros(len_alphabet)
    for i in range(keys_amount):
        for j in range(len_alphabet):
            value = ciphertexts[i][j]
            p_c[value - 1] += p_k[i] * p_m[j]
            
    # P(c|m)
    p_c_m = np.zeros((len_alphabet, len_alphabet))
    for i in range(keys_amount):
        for j in range(len_alphabet):
            value = ciphertexts[i][j]
            p_c_m[j][value - 1] += p_k[i]
    
    # P(m|c)
    p_m_c = np.zeros((len_alphabet, len_alphabet))
    for i in range(len_alphabet):
        for j in range(len_alphabet):
            # print(p_m[i], p_c_m[i][j], p_c[j])
            value = p_m[i] * p_c_m[i][j] / p_c[j]
            p_m_c[i][j] = value
    
    
    # Entropy
    h_m = E(p_m)
    h_k = E(p_k)
    h_c = E(p_c)
    
    leak = h_m + h_k - h_c
    
    do_report(
        "showcase.txt",
        cipher_matrix=ciphertexts,
        p_m_c=p_m_c,
        p_c_m=p_c_m,
        h_m=h_m,
        h_k=h_k,
        h_c=h_c,
        info_leakage=leak,
        p_k=p_k,
        p_m=p_m,
        p_c=p_c,
        alphabet=alphabet
    )
    

if __name__ == "__main__":
    main()