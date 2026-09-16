# from wmf import trust_center, UserWMF

# def main():
#     A = UserWMF("Aboba")
#     B = UserWMF("Biba")
#     A.send_message(B, "abcd")
#     print(A)
#     print(B)
    
# if __name__ == "__main__":
#     main()

import uvicorn
from wmf.trust_center import app

if __name__ == "__main__":
    uvicorn.run(
        app=app, 
        host="0.0.0.0",
        port=8000
    )