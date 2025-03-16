class IndexDict:
    def __init__(self, vec) -> None:
        dict = self.__generate_(vec, False)
        rdict = self.__generate_(vec, True)
        for key, value in list(rdict.items()):
            if self.__contains_(dict, key):
                for ele in value:
                    if ele not in dict[key]:
                        dict[key].append(ele)
            else:
                dict[key] = value
        self.__dict = dict

    def __contains_(self, dic, key):
        if key in list(dic.keys()): return True
        return False

    def __generate_(self, vec, reverse):
        sorted = []
        idx = 1 if reverse else 0

        if len(vec) == 0:
            return {}

        for i in range(len(vec)):
            vertex = vec[i]
            sorted.append(vertex)
        sorted.sort(key=lambda x: x[idx])

        organized, key, value = [], [], []
        current = sorted[0][idx]
        for ele in sorted:
            if ele[idx] != current:
                value.append(organized)
                key.append(current)
                organized = []
                current = ele[idx]
            organized.append(ele[0 if reverse else 1])
        value.append(organized)
        key.append(current)

        return {key[i]: value[i] for i in range(len(key))}

    def insert(self, key, value) -> None:
        if self.contains(key):
            raise KeyError("key already exists")

        self.__dict[key] = value
        for ele in value:
            if self.contains(ele):
                self.find(ele).append(key)
            else:
                self.__dict[ele] = [key]

    def contains(self, key) -> bool:
        if key in list(self.__dict.keys()): return True
        return False
    
    def find(self, key) -> list:
        return self.__dict[key]

    def items(self) -> list:
        return list(self.__dict.items())
