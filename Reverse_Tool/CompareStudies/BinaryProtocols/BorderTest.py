
from common.readdata import *
from BinaryProtocol.Logic.MsgSplitLogic import MegSplitLogic
from common.DataTuning.RawDataTuning.ModBusDataTuning import ModBusDataTuning
from Config.modbus import modbus
from common.analyzer.analyzer_common import base_analyzer
from common.DataTuning.RawDataTuning.FTPDataTuning import FTPDataTuning
from common.Parser.FTPParser import FTPParser
from common.Parser.CombinePaser import ComPaser
from common.Converter.base_convert import Converter
from common.measure_tool.MessaSplitMeasure import MessageSplitMeasure
import sys
from Data_base.Data_redis.redis_deal import redis_deal
from showresult.BoxShow.BoxPlot import *

class BorderTest:
    def __init__(self):
        self.msgLogic = MegSplitLogic()
        self.modbus = ModBusDataTuning()
        self.md = modbus()
        self.anlzer = base_analyzer()
        self.ftp = FTPDataTuning()
        self.ftpPaser = FTPParser()
        self.cmPaser = ComPaser()
        self.cvt = Converter()
        self.mtool = MessageSplitMeasure()
        self.rds = redis_deal()

    def getModHPfone(self):
        self.msgs = self.modbus.getModDatas()
        #vePara = {'diffMeasure': 'abs', 'vWayFre': 'loose', 'T': 0, 'r': 0.3}
        vePara = {'diffMeasure': 'abs', 'vWayFre': 'normal', 'T': 0, 'r': 0.3}
        msgs = self.modbus.getModDatas()
        #Inferborders = self.msgLogic.getFreBorders(vePara, msgs)
        #Inferborders = self.msgLogic.getOrderBorders(vePara, msgs)
        #Inferborders = self.msgLogic.getEntryBorders(vePara, msgs)
        Inferborders = self.msgLogic.getMbourders(vePara, msgs)
        rightBorders = [self.md.GetMessageBorder(msg) for msg in self.msgs]
        i = 0
        print(Inferborders[0], rightBorders[0], msgs[0])
        scores = []
        while(i < len(Inferborders)):
            scores.append(self.anlzer.get_f1(Inferborders[i], rightBorders[i]))
            i = i + 1
        print(sum([score[0] for score in scores]) / len(Inferborders))
        print(sum([score[1] for score in scores]) / len(Inferborders))
        print(sum([score[2] for score in scores]) / len(Inferborders))

    def getModfoneMix(self):
        self.msgs = self.modbus.getModDatas()
        vePara = {'diffMeasure': 'abs', 'vWayFre': 'loose', 'T': 0, 'r': 0.3}
        msgs = self.modbus.getModDatas()
        Inferborders = self.msgLogic.getFreBorders(vePara, msgs)
        InferbordersOne = self.msgLogic.getOrderBorders(vePara, msgs)
        #InferbordersOne = self.msgLogic.getEntryBorders(vePara, msgs)
        Inferborders = self.cvt.MergeListGroup(Inferborders, InferbordersOne)
        rightBorders = [self.md.GetMessageBorder(msg) for msg in self.msgs]
        i = 0
        scores = []
        while (i < len(Inferborders)):
            scores.append(self.anlzer.get_f1(Inferborders[i], rightBorders[i]))
            i = i + 1
        print(sum([score[0] for score in scores]) / len(Inferborders))
        print(sum([score[1] for score in scores]) / len(Inferborders))
        print(sum([score[2] for score in scores]) / len(Inferborders))

    def getFtpMixfone(self):
        msgs = self.ftp.getTotalData()
        vePara = {'diffMeasure': 'abs', 'vWayFre': 'loose', 'T': 0, 'r': 0.3}
        msgs = self.ftpPaser.parseMsgs(msgs)
        Inferborders = self.msgLogic.getFreBorders(vePara, msgs)
        InferbordersOne = self.msgLogic.getOrderBorders(vePara, msgs)
        # InferbordersOne = self.msgLogic.getEntryBorders(vePara, msgs)
        Inferborders = self.cvt.MergeListGroup(Inferborders, InferbordersOne)
        rightBorders = msgs
        i = 0
        scores = []
        while (i < len(Inferborders)):
            scores.append(self.anlzer.get_f1(Inferborders[i], rightBorders[i]))
            i = i + 1
        print(sum([score[0] for score in scores]) / len(Inferborders))
        print(sum([score[1] for score in scores]) / len(Inferborders))
        print(sum([score[2] for score in scores]) / len(Inferborders))

    def getHPFtpfone(self):
        msgs = self.ftp.getTotalData()
        #vePara = {'diffMeasure': 'abs', 'vWayFre': 'loose', 'T': 0, 'r': 0.3}
        vePara = {'diffMeasure': 'abs', 'vWayFre': 'normal', 'T': 0, 'r': 0.3}
        #Inferborders = self.msgLogic.getFreBorders(vePara, msgs)
        Inferborders = self.msgLogic.getOrderBorders(vePara, msgs)
        #Inferborders = self.msgLogic.getEntryBorders(vePara, msgs)
        #Inferborders = self.msgLogic.getMbourders(vePara, msgs)
        #self.rds.insert_to_redis('nowborder', Inferborders)
        #InferbordersOne = self.rds.read_from_redis('nowborder')
        #print(self.mtool.MLs(Inferborders, InferbordersOne))
        rightBorders = self.ftpPaser.parseMsgs(msgs)
        print(Inferborders[0], rightBorders[0], msgs[0])
        i = 0
        scores = []
        while (i < len(Inferborders)):
            scores.append(self.anlzer.get_f1(Inferborders[i], rightBorders[i]))
            i = i + 1
        print(sum([score[0] for score in scores]) / len(Inferborders))
        print(sum([score[1] for score in scores]) / len(Inferborders))
        print(sum([score[2] for score in scores]) / len(Inferborders))

    def getMixFone(self):
        mixMsgs = []
        ftpData = self.ftp.getTotalData()
        modData = self.modbus.getModDatas()
        mixMsgs.extend(ftpData)
        mixMsgs.extend(modData)
        #vePara = {'diffMeasure': 'abs', 'vWayFre': 'loose', 'T': 0, 'r': 0.3}
        vePara = {'diffMeasure': 'abs', 'vWayFre': 'normal', 'T': 0, 'r': 0.3}
        #Inferborders = self.msgLogic.getFreBorders(vePara, mixMsgs)
        Inferborders = self.msgLogic.getOrderBorders(vePara, mixMsgs)
        #Inferborders = self.msgLogic.getEntryBorders(vePara, mixMsgs)
        #Inferborders = self.msgLogic.getMbourders(vePara, mixMsgs)
        rightBorders = self.cmPaser.parseMsgs(mixMsgs)
        print(Inferborders[0], rightBorders[0], str(mixMsgs[0]))
        print(Inferborders[-1], rightBorders[-1], str(mixMsgs[-1]))
        i = 0
        scores = []
        while (i < len(Inferborders)):
            scores.append(self.anlzer.get_f1(Inferborders[i], rightBorders[i]))
            i = i + 1
        print(sum([score[0] for score in scores]) / len(Inferborders))
        print(sum([score[1] for score in scores]) / len(Inferborders))
        print(sum([score[2] for score in scores]) / len(Inferborders))

    def getMixFoneScores(self, vePara, parserType):
        mixMsgs = []
        ftpData = self.ftp.getTotalData()
        modData = self.modbus.getModDatas()
        mixMsgs.extend(ftpData)
        mixMsgs.extend(modData)
        Inferborders = None
        if parserType == 'HP':
            Inferborders = self.msgLogic.getFreBorders(vePara, mixMsgs)
        elif parserType == 'HE':
            Inferborders = self.msgLogic.getEntryBorders(vePara, mixMsgs)
        elif parserType == 'HO':
            Inferborders = self.msgLogic.getOrderBorders(vePara, mixMsgs)
        else:
            Inferborders = self.msgLogic.getMbourders(vePara, mixMsgs)
        rightBorders = self.cmPaser.parseMsgs(mixMsgs)
        i = 0
        scores = []
        while (i < len(Inferborders)):
            scores.append(self.anlzer.get_f1(Inferborders[i], rightBorders[i]))
            i = i + 1
        print(parserType)
        print(sum([score[2] for score in scores]) / len(Inferborders))
        return [score[2] for score in scores]

    def getMixMixFone(self):
        mixMsgs = []
        ftpData = self.ftp.getTotalData()
        modData = self.modbus.getModDatas()
        mixMsgs.extend(ftpData)
        mixMsgs.extend(ftpData)
        vePara = {'diffMeasure': 'abs', 'vWayFre': 'loose', 'T': 0, 'r': 0.3}
        msgs = self.ftpPaser.parseMsgs(mixMsgs)
        InferbordersOne = self.msgLogic.getFreBorders(vePara, msgs)
        Inferborders = self.msgLogic.getOrderBorders(vePara, msgs)
        # InferbordersOne = self.msgLogic.getEntryBorders(vePara, msgs)
        Inferborders = self.cvt.MergeListGroup(Inferborders, InferbordersOne)
        rightBorders = msgs
        i = 0
        scores = []
        while (i < len(Inferborders)):
            scores.append(self.anlzer.get_f1(Inferborders[i], rightBorders[i]))
            i = i + 1
        print(sum([score[0] for score in scores]) / len(Inferborders))
        print(sum([score[1] for score in scores]) / len(Inferborders))
        print(sum([score[2] for score in scores]) / len(Inferborders))



if __name__ == '__main__':
    bdtest = BorderTest()
    veparas = {'diffMeasure': 'abs', 'vWayFre': 'normal', 'T': 0, 'r': 0.3}
    tR = {}
    tR['VE'] = bdtest.getMixFoneScores(veparas, 'VE')
    veparas['vWayFre'] =  'loose'
    tR['HP'] = bdtest.getMixFoneScores(veparas, 'HP')
    tR['HE'] = bdtest.getMixFoneScores(veparas, 'HE')
    tR['HO'] = bdtest.getMixFoneScores(veparas, 'HO')
    plotBox(tR)
    #bdtest.getMixFone()
    #bdtest.getHPFtpfone()
    #bdtest.getModHPfone()
    #bdtest.getMixFone()
    #bdtest.getModfoneMix()
    #bdtest.getFtpMixfone()
    #bdtest.getMixMixFone()

