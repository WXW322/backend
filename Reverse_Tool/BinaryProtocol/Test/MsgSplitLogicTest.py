
from BinaryProtocol.Logic.MsgSplitLogic import MegSplitLogic
from common.readdata import *


class MsgSplitLogicTest:
    def __init__(self):
        self.msgSplit = MegSplitLogic()

    def testDatas(self):
        messages = read_datas('/home/wxw/data/modbusdata', 'single')
        messages = get_puredatas(messages)[0:1000]
        return messages

    def getFreBordersTest(self):
        messages = self.testDatas()
        vePara = {'diffMeasure': 'abs', 'vWayFre': 'loose', 'T': 0, 'r': 0.3}
        print(self.msgSplit.getFreBorders(vePara, messages))

if __name__ == '__main__':
    msgSplt = MsgSplitLogicTest()
    msgSplt.getFreBordersTest()