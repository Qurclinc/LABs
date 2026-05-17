from services import RSAClient, ElgamalCleint
from utils import encode_text, decode_text, verify_primality, get_primitive_root

if __name__ == "__main__":
    
    cl1 = ElgamalCleint(32)
    cl2 = ElgamalCleint(32)
    ElgamalCleint.exchange(cl1, cl2)
    text = "aboba c"
    msg = encode_text(text, "eng")
    ct = cl1.send_message(msg)
    print(ct)
    pt = cl2.read_message(ct)
    msg = decode_text(pt, "eng")
    print(msg)
    
    # cl1 = RSAClient()
    # cl2 = RSAClient()
    
    # print(cl1.public_key)
    # print(cl2.public_key)
    # RSAClient.exchange(cl1, cl2)
    
    # text = "aboba"
    # msg = encode_text(text, "eng")
    # ct = cl1.send_message(msg)
    # print(ct)
    # pt = cl2.read_message(ct)
    # msg = decode_text(pt, "eng")
    # print(msg)