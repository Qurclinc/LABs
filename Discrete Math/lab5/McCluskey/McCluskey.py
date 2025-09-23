from typing import List

class McCluskey:
    def __init__(self, func: List[int]):
        self.init_list(func)

    def init_list(self, func: List[int]):
        self.list = [bin(num)[2:] for num in func]

    def __str__(self):
        return "\n".join([num.zfill(4) for num in self.list])