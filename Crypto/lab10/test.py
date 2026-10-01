from core.rsa import RSA
from utils import encode_text, decode_text, h

LANG = "eng"

rsa = RSA(128)

# rsa.generate_keys()
# rsa.save_keys()
# rsa.load_privkey()

# rsa.sign(
#     encode_text("XOR", LANG),
#     lang=LANG
# )

# rsa.load_pubkey()
# with open("./out/message.txt", "r") as msg, open("./out/sign.txt", "r") as sign:
#     M = encode_text(msg.read(), LANG)
#     S = int(sign.read())
#     M2 = rsa.verify_sign(S, M)
#     print(M2)

# ---

# rsa.load_privkey()
# rsa.sign(
#     encode_text("XOR", LANG),
#     lang=LANG,
#     p=107
# )

# rsa.load_pubkey()
# with open("./out/message.txt", "r") as msg, open("./out/sign.txt", "r") as sign:
#     M = encode_text(msg.read(), lang=LANG)
#     S = int(sign.read())
#     hM = h(M, 107)
#     print(hM)
#     print(rsa.verify_sign(S, hM))