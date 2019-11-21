
from common.readdata import *
from BinaryProtocol.Logic.MsgSplitLogic import MegSplitLogic
from common.DataTuning.RawDataTuning.ModBusDataTuning import ModBusDataTuning
from Config.modbus import modbus
from common.analyzer.analyzer_common import base_analyzer

class BorderTest:
    def __init__(self):
        self.msgLogic = MegSplitLogic()
        self.modbus = ModBusDataTuning()
        self.md = modbus()
        self.anlzer = base_analyzer()

    def getHPfone(self):
        self.msgs = self.modbus.getModDatas()
        vePara = {'diffMeasure': 'abs', 'vWayFre': 'loose', 'T': 0, 'r': 0.3}
        msgs = self.modbus.getModDatas()
        Inferborders = self.msgLogic.getFreBorders(vePara, msgs)
        rightBorders = [self.md.GetMessageBorder(msg) for msg in self.msgs]
        i = 0
        scores = []
        while(i < len(Inferborders)):
            scores.append(self.anlzer.get_f1(Inferborders[i], rightBorders[i]))
            i = i + 1
        print(sum([score[2] for score in scores]) / len(Inferborders))
        print(sum([score[0] for score in scores]) / len(Inferborders))
        print(sum([score[1] for score in scores]) / len(Inferborders))

if __name__ == '__main__':
    bdtest = BorderTest()
    bdtest.getHPfone()

