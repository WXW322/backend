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


class MegSplitLogic:
    def __init__(self):
        super().__init__()
        self.converter = Converter()
        self.msgSpliter = MsgSpliter()
        self.redis_dealer = redis_deal()
        self.splt = splitter()
        self.desiner = Desiner()

    def getOrderBorders(self):
        pass

    def getEntryBorders(self):
        pass

    def getMbourders(self):
        pass

    def getFreBorders(self, gveConfigParas, messages):
        freDicts = self.splt.getFreVotesByMsg(messages)
        paraFre = {}
        paraFre['diff_measure'] = gveConfigParas['diffMeasure']
        paraFre['vWay'] = gveConfigParas['vWayFre']
        paraFre['T'] = gveConfigParas['T']
        paraFre['r'] = gveConfigParas['r']
        return self.desiner.VoteMultyByDicParas(paraFre, freDicts)





