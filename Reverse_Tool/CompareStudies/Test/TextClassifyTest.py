
from CompareStudies.TextTools.TextClassify import TextClassify
from common.readdata import *

class TextClassifyTest:
    def __init__(self, messages):
        self.textClassify = TextClassify(messages)

    def TestWordsFind(self, wSize, TK, wLen):
        return self.textClassify.cntWord(wSize, TK, wLen)

    def TestWordsPro(self, wSize, TK, wLen):
        self.textClassify.cntWord(wSize, TK, wLen)
        print(self.textClassify.cntPro())

    def TestFeatureGene(self, wSize, TK, wLen):
        self.textClassify.cntWord(wSize, TK, wLen)
        self.textClassify.cntPro()
        print(self.textClassify.FeGenerator())

    def clsDatasTest(self, wSize, TK, wLen, K):
        resultMs = self.textClassify.clsMessages(wSize, TK, wLen, K)
        for cls in resultMs:
            print(cls)
            for data in resultMs[cls]:
                print(str(data))
            print('mmm')


if __name__ == '__main__':
    messages = read_datas('/home/wxw/data/httpDatas/http_measure', 'single')
    messages = get_puredatas(messages)
    textCls = TextClassifyTest(messages)
    print(textCls.clsDatasTest(3, 8, 3, 5))
    #print(textCls.TestFeatureGene(3, 5, 5))
    #print(textCls.TestWordsPro(3, 5, 5))
