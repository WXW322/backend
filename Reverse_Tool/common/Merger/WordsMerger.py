from common.measure_tool.DisWords import DisWords
import sys

class WordsMerger:
    def __init__(self, words=None):
        self.wordsDis = DisWords()
        self.words = words

    def mergeWord(self, wA, wB, lo):
        preWLen = len(wA) - lo
        preW = wA[0:preWLen]
        mergeW = preW + wB
        return mergeW

    def mergeWords(self, words):
        while(len(words) > 1):
            wList = self.wordsDis.measureWList(words)
            lo_min_x = -1
            lo_min_y = -1
            min_V = 0
            for i in range(len(words)):
                for j in range(len(words)):
                    if wList[i][j] > min_V:
                        min_V = wList[i][j]
                        lo_min_x = i
                        lo_min_y = j
            if lo_min_x != -1:
                xMin = min(lo_min_x, lo_min_y)
                xMax = max(lo_min_x, lo_min_y)
                wordNew = self.mergeWord(words[lo_min_x], words[lo_min_y], min_V)
                del words[xMin]
                del words[xMax-1]
                words.append(wordNew)
            else:
                break
        words = ['_'.join(word) for word in words]
        return words
