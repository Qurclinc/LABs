class Set:

    def __init__(self, arr=[]):
        self.arr = []
        for i in arr:
            if i not in self.arr:
                self.arr += [i]

    def add(self, elem):
        if elem not in self.arr:
            self.arr += [elem]

    def remove(self, elem):
        self.arr.remove(self.arr.index(elem))

    @staticmethod
    def Intersect(first, second):
        return Set([i for i in first.arr if i in second.arr] + [i for i in second.arr if i in first.arr])

    @staticmethod
    def Unite(first, second):
        return Set([i for i in first.arr] + [i for i in second.arr])

    @staticmethod
    def Differ(first, second):
        return Set([i for i in first.arr if i not in second.arr])

    @staticmethod
    def Product(first, second):
        arr1, arr2 = first.arr, second.arr
        result = Set()
        for e1 in arr1:
            for e2 in arr2:
                couple = (e1, e2)
                result.add(couple)
        return result
    
    @staticmethod
    def GetBoolean(set):
        result = Set()
        result.add("Ø")
        for variant in range (1, 2**len(set.arr)):
            number = bin(variant)[2:]
            number = "0" * (len(set.arr) - len(number)) + number
            tmp = Set()
            for i, sym in enumerate(number):
                # print(number, i, sym)
                if sym == "1": tmp.add(set.arr[i])
            result.add(tmp)
        return result     
    

    @staticmethod
    def Xor(first, second):
        D1 = Set.Differ(first, second)
        D2 = Set.Differ(second, first)
        return Set.Unite(D1, D2)




    def __str__(self):
        return "{" + ", ".join(map(str, self.arr)) + "}"

