
from CompareStudies.TextTools.TextFormInfer import TextFormInfer
from common.readdata import *

class TextFormInferTest:
    def __init__(self, messages):
        self.tFomInfer = TextFormInfer(messages)

    def ldaFormatInferTest(self, wSize, TK, wLen, Kcls):
        fNums = self.tFomInfer.ldaFormatInfer(wSize, TK, wLen, Kcls)
        for fnum in fNums:
            print(fnum._str_debug())


if __name__ == '__main__':
    messages = read_datas('/home/wxw/data/httpDatas/http_measure', 'single')
    messages = get_puredatas(messages)
    textFormattest = TextFormInferTest(messages)
    textFormattest.ldaFormatInferTest(3, 8, 3, 5)