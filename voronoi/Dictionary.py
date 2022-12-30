class IndexDict:
    def __init__(self, vec) -> None:
        dict = self.__generate_(vec, False)
        rdict = self.__generate_(vec, True)
        for key, value in list(rdict.items()):
            if self.__contains_(dict, key):
                for ele in value:
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

    def contains(self, key) -> bool:
        if key in list(self.__dict.keys()): return True
        return False
    
    def find(self, key) -> list:
        return self.__dict[key]

    def items(self) -> list:
        return list(self.__dict.items())
