from common.Spliter.VE_spliter import splitter
from common.Converter.base_convert import Converter
from ngrambuild.Desiner import Desiner
from common.Spliter.MsgSpliter import MsgSpliter
import sys
from Data_base.Data_redis.redis_deal import redis_deal
import json
from common.Spliter.vertical_splitter import vertical_splitter
from common.Merger.base_merger import base_merger
from ngrambuild.pyngram import voters
from common.measure_tool.MeasureAb import MeasureAb
from common.Converter.base_convert import Converter
from common.DataTuning.RawDataTuning.DataTuning import DataTuning

class MegSplitLogic:
    def __init__(self):
        super().__init__()
        self.converter = Converter()
        self.msgSpliter = MsgSpliter()
        self.redis_dealer = redis_deal()
        self.splt = splitter()
        self.desiner = Desiner()
        self.msAb = MeasureAb()
        self.cvt = Converter()
        self.dataTuning = DataTuning()

    def getOrderBorders(self, gveConfigParas, messages):
        borderDicts = self.splt.getOrderVotesByMsgs(messages)
        paraFre = {}
        paraFre['diff_measure'] = gveConfigParas['diffMeasure']
        paraFre['vWay'] = gveConfigParas['vWayFre']
        paraFre['T'] = gveConfigParas['T']
        paraFre['r'] = gveConfigParas['r']
        return self.desiner.VoteMultyByDicParas(paraFre, borderDicts)

    def getEntryBorders(self, gveConfigParas, messages):
        entryDicts = self.splt.getEntryVotesByMsgs(messages)
        paraFre = {}
        paraFre['diff_measure'] = gveConfigParas['diffMeasure']
        paraFre['vWay'] = gveConfigParas['vWayFre']
        paraFre['T'] = gveConfigParas['T']
        paraFre['r'] = gveConfigParas['r']
        return self.desiner.VoteMultyByDicParas(paraFre, entryDicts)

    def getMbourders(self, gveConfigParas, messages):
        VeDicts = self.splt.getVeVotesByMsg(messages)
        paraFre = {}
        paraFre['diff_measure'] = gveConfigParas['diffMeasure']
        paraFre['vWay'] = gveConfigParas['vWayFre']
        paraFre['T'] = gveConfigParas['T']
        paraFre['r'] = gveConfigParas['r']
        print(VeDicts[0])
        return self.desiner.VoteMultyByDicParas(paraFre, VeDicts)

    def getFreBorders(self, gveConfigParas, messages):
        freDicts = self.splt.getFreVotesByMsg(messages)
        paraFre = {}
        paraFre['diff_measure'] = gveConfigParas['diffMeasure']
        paraFre['vWay'] = gveConfigParas['vWayFre']
        paraFre['T'] = gveConfigParas['T']
        paraFre['r'] = gveConfigParas['r']
        return self.desiner.VoteMultyByDicParas(paraFre, freDicts)

    def msgSplit(self, borders, msgs, maxRange=15):
        return self.msgSpliter.splitMessages(borders, msgs, maxRange)


    def getOrderBordersNyPath(self, filePath='', msgs=None, maxRange=15):
        # future update
        veParas = {'diffMeasure': 'abs', 'vWayFre': 'loose', 'T': 0, 'r': 0.3}
        # future update
        #if filePath != '':
        #    msgs = self.dataTuning.readDatas(filePath)
        borders = self.getOrderBorders(veParas, msgs)
        spltMsgs = self.msgSplit(borders, msgs, maxRange)
        return borders, spltMsgs






