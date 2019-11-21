
from ngrambuild.pyngram import voters
from common.readdata import *

class pyngramTest:
    def __init__(self):
        self.vv = voters()

    def TestRawWords(self):
        messages = read_datas('/home/wxw/data/modbusdata', 'single')
        messages = get_puredatas(messages)[0:10]
        print(self.vv.getQueryMsgWords(messages))


if __name__ == '__main__':
    pTest = pyngramTest()
    pTest.TestRawWords()