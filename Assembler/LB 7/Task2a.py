def do_crypt(text, gamma):
    result = []
    gamma_ptr = 0
    
    for char in text:
        
        gamma_char = gamma[gamma_ptr % len(gamma)]
        
        encrypted_char = chr(ord(char) ^ ord(gamma_char))
        result.append(encrypted_char)
        gamma_ptr += 1
    
    return ''.join(result)

def main():
    
    text = input("Enter text: ")
    gamma = input("Enter gamma: ")
    
    
    encrypted = do_crypt(text, gamma)
    
    
    print(f"\nOriginal text: {text}")
    print(f"Original gamma: {gamma}")
    print(f"Encrypted: {encrypted}")
    
    
    decrypted = do_crypt(encrypted, gamma)
    print(f"Decrypted: {decrypted}")

if __name__ == "__main__":
    main()