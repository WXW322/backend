
from CompareStudies.TextTools.TextClassify import TextClassify
from common.readdata import *
from common.DataTuning.RawDataTuning.HttpDataTuning import HttpDataTuning
from common.DataTuning.RawDataTuning.FTPDataTuning import FTPDataTuning
from itertools import chain
from common.Classify.Dbscan import DbScanClasser

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
        features = self.textClassify.FeGenerator()
        print(features)
        return features


    def clsDatasTest(self, wSize, TK, wLen, K):
        resultMs = self.textClassify.clsMessages(wSize, TK, wLen, K)
        for cls in resultMs:
            print(cls)
            for data in resultMs[cls]:
                print(str(data))
            print('mmm')

    def clsDbscanTest(self, wSize, TK, wLen, minDis, minPt):
        resultMs = self.textClassify.clsByDbscan(wSize, TK, wLen, minDis, minPt)
        for cls in resultMs:
            print(cls)
            for data in resultMs[cls]:
                print(str(data))
            print('mmm')


if __name__ == '__main__':
    ftpDATAtuning = FTPDataTuning()
    srcMsgs, desMsgs = ftpDATAtuning.tuningHttpByregix()
    textCls = TextClassifyTest(srcMsgs)
    textCls.clsDatasTest(3, 15, 3, 15)
    """
    httpDataTuning = HttpDataTuning()
    srcMsgs, desMsgs = httpDataTuning.tuningHttpByregix()
    textCls = TextClassifyTest(srcMsgs)
    textCls.clsDbscanTest(3, 5, 5, 0.05, 10)
    """
    """
    dataF = textCls.TestFeatureGene(3, 5, 5)
    dbscan = DbScanClasser()
    disLists = dbscan.caculateEuras(dataF)
    disLists = list(chain.from_iterable(disLists))
    minData = min(disLists)
    maxData = max(disLists)
    print(minData, maxData)
    """
    """
    messages = read_datas('/home/wxw/data/httpDatas/http_measure', 'single')
    messages = get_puredatas(messages)
    textCls = TextClassifyTest(messages)
    
    print(textCls.clsDatasTest(3, 8, 3, 5))
    #print(textCls.TestFeatureGene(3, 5, 5))
    #print(textCls.TestWordsPro(3, 5, 5))
    """