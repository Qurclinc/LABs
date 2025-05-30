def get_bytes(word):
    word = word.encode("ASCII")
    return " ".join(f"{byte:08b}" for byte in word)

def get_from_bytes(b_word):
    return "".join(chr(int(byte, 2)) for byte in b_word.split())

def change_bits(byte, bit1, bit2):
    byte = list(byte)[::-1]
    byte[bit1], byte[bit2] = byte[bit2], byte[bit1]
    return "".join(byte[::-1])

def do_crypt(b_word):
    res = []
    for byte in b_word.split():
        byte = change_bits(byte, 1, 3)
        byte = change_bits(byte, 4, 7)
        res += [byte]
    return " ".join(res)

def main():
    word = input()
    print(f"Source word: {word}")
    b_word = get_bytes(word)
    print(f"Source bytes:\t {b_word}")
    encrypted_bytes = do_crypt(b_word)
    print(f"Encrypted bytes: {encrypted_bytes}")
    encrypted_word = get_from_bytes(encrypted_bytes)
    print(f"Encrypted word: {encrypted_word}")
    decrypted_bytes = do_crypt(encrypted_bytes)
    print(f"Decrypted bytes: {decrypted_bytes}")
    decrypted_word = get_from_bytes(decrypted_bytes)
    print(f"Decrypted word: {decrypted_word}")

if __name__ == "__main__":
    main()