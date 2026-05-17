import os
from pathlib import Path
from Services.crypter import Crypter

cr = Crypter()
cr.set_key(Path("/home/bill/Pictures/blanka.jpg"))

# cr.encrypt(Path("/home/bill//Pictures/M43s7r0.jpg"), Path("./test.pixcrypted"))

res = cr.decrypt(Path("./test.pixcrypted"), Path("./src.jpg"))
print(res)

# cr.encrypt(Path("./test.mp4").absolute(), Path("./test2.pixcrypted").absolute())

# cr.decrypt(Path("./test2.pixcrypted").absolute(), Path("./test_dec.mp4").absolute())


# def proceed_chunk():
#     CHUNK_SIZE = 4 * 1024
#     filepath = Path("./test.mp4").absolute()
#     with open(filepath, "rb") as file:
#         while True:
#             chunk = file.read(CHUNK_SIZE)
#             if not chunk:
#                 break
#             yield chunk
# for chunk in proceed_chunk():
#     print(chunk)