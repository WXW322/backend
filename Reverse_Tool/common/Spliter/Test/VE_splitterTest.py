
from common.Spliter.VE_spliter import splitter
from common.readdata import *


class VE_spliterTest:
    def __init__(self):
        self.spt = splitter()

    def TestFreWords(self, messages):
        return self.spt.getFreVotesByMsg(messages)

    def TestOrderWords(self, messages):
        return self.spt.getOrderVotesByMsgs(messages)

if __name__ == '__main__':
    messages = read_datas('/home/wxw/data/modbusdata', 'single')
    messages = get_puredatas(messages)[0:1000]
    vtest = VE_spliterTest()
    vtest.TestOrderWords(messages)
    #print(vtest.TestFreWords(messages))