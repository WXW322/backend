
import functools

class BaseRankModel:
    def __init__(self):
        pass
    @staticmethod
    def comPareWordsStrategy(w1, w2):
        if w1[2] < w2[2]:
            return 1
        elif w1[1] > w2[1]:
            return -1
        else:
            if w1[0] < w2[0]:
                return 1
            elif w1[0] > w2[0]:
                return -1
            else:
                return 0

    @staticmethod
    def sortList(L):
        sorted(L, key = functools.cmp_to_key(BaseRankModel.comPareWordsStrategy))
        return L


if __name__ == '__main__':
    mm = BaseRankModel()
    ll = [('aaa', 10, 0), ('bbb', 1, 2), ('ccc', 10, 3)]
    print(mm.sortList(ll))