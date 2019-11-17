
from common.Merger.WordsMerger import WordsMerger
import sys

class Test:
    def __init__(self):
        self.wMerger = WordsMerger(['aaa', 'bbb'])

    def mergeWords(self, wA, wB, lo):
        return self.wMerger.mergeWord(wA, wB, lo)

    def mergeWordsList(self, words):
        wordsList = [word.split('_') for word in words]
        return self.wMerger.mergeWords(wordsList)




if __name__ == '__main__':
    wTest = Test()
    print(wTest.mergeWordsList(['1_0_3', '0_3_3']))
