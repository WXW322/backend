from common.Spliter.VE_spliter import splitter
from common.Converter.base_convert import Converter
from ngrambuild.Desiner import Desiner
from common.Spliter.MsgSpliter import MsgSpliter
import sys
from Data_base.Data_redis.redis_deal import redis_deal
import json
from common.Spliter.vertical_splitter import vertical_splitter
from common.Merger.base_merger import base_merger
from Config.UserConfig import UserConfig
from IcsProtocol.Config.GveConf import GveConf


class GvoterLogic(splitter):
    def __init__(self):
        super().__init__()
        self.converter = Converter()
        self.msgSpliter = MsgSpliter()
        self.redis_dealer = redis_deal()

    def getGVotes(self, configParas, messages):
        freVotes = self.getFreVotes(configParas, messages)
        entryVotes = self.getEntryVotes(configParas, messages)
        freGVotes = self.converter.MergeListDics(freVotes)
        entryGVotes = self.converter.MergeListDics(entryVotes)
        return freGVotes, entryGVotes

    def getBoundaries(self, configParas, gveConfigParas, messages):
        freGVotes, entryGVotes = self.getGVotes(configParas, messages)
        desiner = Desiner()
        paraFre = {}
        paraFre['diff_measure'] = gveConfigParas['diffMeasure']
        paraFre['vWay'] = gveConfigParas['vWayFre']
        paraFre['T'] = gveConfigParas['T']
        paraFre['r'] = gveConfigParas['r']
        freBoundaries = desiner.VoteSingleByDicParas(paraFre, freGVotes)
        paraFre['vWay'] = gveConfigParas['vWayEntry']
        entryBoundaries = desiner.VoteSingleByDicParas(paraFre, entryGVotes)
        return Converter().MergeLists(freBoundaries, entryBoundaries)

    def getCommonRange(self, messages):
        heads = [len(message) for message in messages]
        t_head = min(heads)
        t_fhead = min(23, t_head + 2)
        return t_fhead

    def filterBoundaries(self, boundaries, cRange):
        rBoundaries = []
        for boundary in boundaries:
            if boundary < cRange:
                rBoundaries.append(boundary)
            else:
                break
        return rBoundaries

    def getGBoundaries(self, boundaries, messages):
        cRange = self.getCommonRange(messages)
        cBoundaries = self.filterBoundaries(boundaries, cRange)
        vSpliter = vertical_splitter(messages)
        merGer = base_merger()

        return cBoundaries

    def getSplitMessages(self, configParas, gveConfigParas, messages):
        splitKey = '{}_{}'.format(configParas.getUserPathDynamic(), 'GSplit')
        gBoundaries = None
        if self.redis_dealer.is_exist_key(splitKey):
            gBoundaries = json.loads(self.redis_dealer.read_from_redis(splitKey))
        else:
            boundaries = self.getBoundaries(configParas, gveConfigParas, messages)
            gBoundaries = self.getGBoundaries(boundaries, messages)
            jsongBoundaries = json.dumps(gBoundaries)
            self.redis_dealer.insert_to_redis(splitKey, jsongBoundaries)
        return gBoundaries



    def splitMessages(self, configParas, gveConfigParas, messages):
        gBoundaries = self.getSplitMessages(configParas, gveConfigParas, messages)
        return self.msgSpliter.splitMessages([gBoundaries for i in range(len(messages))], messages)

    def splitFileMessages(self, filePath, messages):
        gVeParas = GveConf.geneGveParas()
        uConfig = UserConfig('/home/wxw/data/ToolDatas/15895903730.10.222', '15895903730')
        messageSplitSums = self.splitMessages(uConfig, gVeParas, messages)
        return messageSplitSums









