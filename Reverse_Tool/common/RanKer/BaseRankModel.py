
import functools

class BaseRankModel:
    def __init__(self):
        pass
    @staticmethod
    def comPareWordsStrategy(w1, w2):
        if w1[1] < w2[1]:
            return 1
        elif w1[0] > w2[0]:
            return -1
        else:
            if w1[1] > w2[1]:
                return 1
            elif w1[1] < w2[1]:
                return -1
            else:
                return 0

    @staticmethod
    def sortList(L):
        sorted(L, key = functools.cmp_to_key(BaseRankModel.comPareWordsStrategy))

