
from common.Sorter.BaseSort import BaseSort

class TestBaseSort:
    def __init__(self):
        self.bsort = BaseSort()
        pass

    def TestLSort(self):
        L = ['aaa', 'bbb', 'ded']
        return self.bsort.sortList(L)

    def TestSortDic(self):
        ddd = {'aaa' : 1, 'bbb': 2}
        return self.bsort.sortDic(ddd)

    def Testtuple(self):
        ccc = [('aaa', 1), ('bbb', 2)]
        return  self.bsort.sortTulples(ccc)


if __name__ == '__main__':
    tBase = TestBaseSort()
    #print(tBase.TestLSort())
    print(tBase.Testtuple())