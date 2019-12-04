

class BaseSort:
    def __init__(self):
        pass

    def sortList(self, LS):
        return sorted(LS)

    def sortDic(self, dics):
        return sorted(dics.items(), key=lambda x:x[0])

    def sortTulples(self, tuples):
        return sorted(tuples, key=lambda x:x[0])