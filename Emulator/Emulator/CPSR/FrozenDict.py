from collections import Mapping

class FrozenDict(Mapping):
    
    def __init__(self, data):
        self.__data = data

    def __getitem__(self, key): 
        return self.__data[key]

    def __len__(self):
        return len(self.__data)

    def __iter__(self):
        return iter(self.__data)
