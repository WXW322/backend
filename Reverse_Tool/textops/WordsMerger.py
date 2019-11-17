
class WordsMerger:
    def __init__(self):
        pass

    def isContain(self, wA, wB):
        lenMin = min(len(wA), len(wB))
        lo  =  -1
        for i in range(1, lenMin):
            if(i < lenMin and wA[-i:-1] + wA[-1] == wB[0:i]):
                lo = i
            i = i + 1
        return lo

    def mergeWord(self, wA, wB, lo):
        return wA[0:lo] + wB


    def mergeWords(self, words):
        wSet = set()
        for word in words:
            if word not in wSet:
                wSet.add(word)
        wList = list(wSet)

