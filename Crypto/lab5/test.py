# import pprint
# from core import find_eea, find_gea
# from core import binary_pow
# from core import find_multiplicative_inverse
# from core import single_comparision, system_complarisions

# print(single_comparision(65, (-54 % 11), 11))

# system_complarisions([(3, 5), (6, 13), (4, 11), (7, 9)])


import requests

HOST = "localhost"
PORT = "8000"

response = requests.post(f"http://{HOST}:{PORT}/api/eea", json={"a": -117, "b": -51})
print(response.json())

response = requests.post(f"http://{HOST}:{PORT}/api/gea", json={"list": [15,-12,18,6,-27]})
print(response.json())

response = requests.post(f"http://{HOST}:{PORT}/api/pow", json={"a": 84, "n": 78, "m": 897})
print(response.json())

response = requests.post(f"http://{HOST}:{PORT}/api/inverse", json={"a": 75, "m": 881, "forceEEA": False})
print(response.json())

response = requests.post(
    f"http://{HOST}:{PORT}/api/comparision/single",
    json={"a": 15, "b": 18, "m": 127}
)
print(response.json())

response = requests.post(
    f"http://{HOST}:{PORT}/api/comparision/system",
    json={"coeffs": [[3, 5], [6, 13], [4, 11], [7, 9]]}
)
print(response.json())

response = requests.post(
    f"http://{HOST}:{PORT}/api/jacobi",
    json={"a": 146, "n": 311}
)
print(response.json())

## Test value: 11893240203458259617 - prime
response = requests.post(
    f"http://{HOST}:{PORT}/api/devision",
    json={"n": 101}
)
print(response.json())


response = requests.post(
    f"http://{HOST}:{PORT}/api/strassen",
    json={"n": 101, "k": 25}
)
print(response.json())


response = requests.post(
    f"http://{HOST}:{PORT}/api/rabin",
    json={"n": 11893240203458259617, "k": 105}
)
print(response.json())

