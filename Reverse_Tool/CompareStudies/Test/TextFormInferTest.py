
from CompareStudies.TextTools.TextFormInfer import TextFormInfer
from common.readdata import *
from common.Converter.MessageConvert import MessageConvert
from common.DataTuning.RawDataTuning.HttpDataTuning import HttpDataTuning
from common.DataTuning.RawDataTuning.FTPDataTuning import FTPDataTuning
import sys

class TextFormInferTest:
    def __init__(self, messages):
        self.tFomInfer = TextFormInfer(messages)
        self.httpdata = HttpDataTuning()
        self.ftpData = FTPDataTuning()

    def ldaFormatInferTest(self, wSize, TK, wLen, Kcls):
        fNums = self.tFomInfer.ldaFormatInfer(wSize, TK, wLen, Kcls)
        for fnum in fNums:
            print(fnum._str_debug())

    def ladDbscanFormatInfer(self, wSize, TK, wLen, mindis, minpt):
        fNums = self.tFomInfer.ladDbscanFormatInfer(wSize, TK, wLen, mindis, minpt)
        for fnum in fNums:
            print(fnum._str_debug())

    def httpDataTest(self):
        srcDatas, desDatas = self.httpdata.tuningHttpByregix()
        self.tFomInfer = TextFormInfer(desDatas)
        self.ldaFormatInferTest(3, 15, 2, 4)

    def httpDataTestDBS(self):
        httpDataTuning = HttpDataTuning()
        srcMsgs, desMsgs = httpDataTuning.tuningHttpByregix()
        self.tFomInfer = TextFormInfer(desMsgs)
        self.ladDbscanFormatInfer(3, 5, 3, 0.15, 4)

    def ftpDataTest(self):
        srcDatas, desDatas = self.ftpData.tuningHttpByregix()
        self.tFomInfer = TextFormInfer(srcDatas)
        self.ldaFormatInferTest(3, 15, 3, 15)

    def ftpDataTestDBS(self):
        httpDataTuning = FTPDataTuning()
        srcMsgs, desMsgs = httpDataTuning.tuningHttpByregix()
        print(len(srcMsgs) + len(desMsgs))
        self.tFomInfer = TextFormInfer(desMsgs)
        sys.exit()
        self.ladDbscanFormatInfer(3, 15, 3, 0.01, 4)


if __name__ == '__main__':
    textFTest = TextFormInferTest(['aaa'])
    #textFTest.ftpDataTestDBS()
    #textFTest.ftpDataTest()
    textFTest.httpDataTestDBS()
    #textFTest.httpDataTest()
    """
    datas = read_datas('/home/wxw/data/ftp/ftpData', 'multy')
    datasF = []
    for data in datas:
        if len(data) < 100:
            datasF.extend(data)
        else:
            datasF.extend(data[0:500])
    srcDatasF, desDatasF = MessageConvert.clsMessageByDire(datasF)
    srcdatas = get_puredatas(srcDatasF)
    desdatas = get_puredatas(desDatasF)
    srctextFormattest = TextFormInferTest(srcdatas)
    #srctextFormattest.ldaFormatInferTest(3, 8, 3, 5)
    destextFormattest = TextFormInferTest(desdatas)
    #destextFormattest.ldaFormatInferTest(3, 3, 3, 5)
    #destextFormattest.ldaFormatInferTest(3, 3, 3, 5)
    """
    """
    messages = read_datas('/home/wxw/data/httpDatas/http_measure', 'single')
    messages = get_puredatas(messages)
    textFormattest = TextFormInferTest(messages)
    textFormattest.ldaFormatInferTest(3, 8, 3, 5)
    """
