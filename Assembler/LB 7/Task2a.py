def get_bytes(word):
    word = word.encode("ASCII")
    return " ".join(f"{byte:08b}" for byte in word)

def get_from_bytes(b_word):
    return "".join(chr(int(byte, 2)) for byte in b_word.split())

def do_crypt(b_word, gamma):
    res = []
    for byte in b_word.split():
        res += [f"{(int(byte, 2) ^ int(gamma, 2)):08b}"]
    return " ".join(res)

def main():
    word = input()
    print(f"Source word: {word}")
    b_word = get_bytes(word)
    print(f"Source bytes:\t {b_word}")
    gamma = input()[:8]
    print(f"Gamma:\t\t {gamma}")
    encrypted_bytes = do_crypt(b_word, gamma)
    print(f"Encrypted bytes: {encrypted_bytes}")
    encrypted_word = get_from_bytes(encrypted_bytes)
    print(f"Encrypted word: {encrypted_word}")
    decrypted_bytes = do_crypt(encrypted_bytes, gamma)
    print(f"Decrypted bytes: {decrypted_bytes}")
    decrypted_word = get_from_bytes(decrypted_bytes)
    print(f"Decrypted word: {decrypted_word}")

if __name__ == "__main__":
    main()