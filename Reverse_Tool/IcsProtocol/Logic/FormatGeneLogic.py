
from IcsProtocol.Logic.GVoterLogic import GvoterLogic
from common.FieldTypeInfer.WholeFieldTypeInfer import WholeFieldTypeInfer
from Config.UserConfig import UserConfig
from IcsProtocol.Config.GveConf import GveConf
from common.FieldTypeInfer.WholeFieldTypeInfer import WholeFieldTypeInfer
from common.Converter.base_convert import Converter
from IcsProtocol.Logic.ReAjustLogic import ReAjustLogic
from common.Converter.word_converter import word_convert
from common.Spliter.MsgSpliter import MsgSpliter
from common.DataTuning.RawDataTuning.DataTuning import DataTuning
from common.readdata import *
import sys
from IcsProtocol.Logic.IcsSymbolToTree import IcsSymbolToTree


class FormatGeneLogic:
    def __init__(self, messages=None):
        self.messages = messages
        self.wordTypeInfer = WholeFieldTypeInfer(self.messages)
        self.cvter = Converter()
        self.wcvter = word_convert()
        self.msgSplt = MsgSpliter()
        self.dataTuning = DataTuning()
        self.icsSymTree = IcsSymbolToTree()

    def getRanges(self, messages):
        L_len = 65536
        for message in messages:
            if len(message) < L_len:
                L_len = len(message)
        return min(23, L_len + 2)

    def getMesFormat(self):
        pass


    def sortWordsType(self, words):
        words = sorted(words.items(), key = lambda x: x[0][0])
        return words


    def getGFormat(self, congigParas, gVeparas):
        gVoterLogic = GvoterLogic()
        boundaries = gVoterLogic.getSplitMessages(congigParas, gVeparas, self.messages, FType='G')
        boundaries = self.cvter.border2item(boundaries)
        fRange = self.getRanges(self.messages)
        LoRdj = ReAjustLogic(boundaries, self.messages)
        LoRdj.reSplit()
        LoRdj.reCluster()
        boundaries = LoRdj.words
        wordsType = self.wordTypeInfer.extractWords(boundaries, fRange)
        wordsType = self.sortWordsType(wordsType)
        boundaries = self.wcvter.itemtoborder(boundaries)
        return boundaries, wordsType

    def getCFormat(self, configParas, gVeparas, msgs):
        if len(msgs) < 10:
            return [((0, -1), 7)]
        gVoterLogic = GvoterLogic()
        boundaries = gVoterLogic.getSplitMessages(configParas, gVeparas, msgs, FType='C')
        boundaries = self.cvter.border2item(boundaries)
        #print('ss')
        #print(len(msgs))
        #print(msgs[0])
        #print(boundaries)
        #print('ee')
        fRange = self.getRanges(msgs)
        boundaries = self.cvter.filterB(boundaries, fRange)
        LoRdj = ReAjustLogic(boundaries, msgs)
        LoRdj.reSplit()
        LoRdj.reCluster()
        boundaries = LoRdj.words
        cWordTypeInfer = WholeFieldTypeInfer(msgs)
        wordsType = cWordTypeInfer.extractCWords(boundaries)
        wordsType = self.sortWordsType(wordsType)
        return wordsType

    def clsByFunc(self, los):
        tCls = {}
        for msg in self.messages:
            tFunc = msg[los[0]:los[1]]
            if tFunc not in tCls:
                tCls[tFunc] = []
            tCls[tFunc].append(msg[los[1]:])
        return tCls

    def GTreeGenerate(self, configParas, gVeparas):
        _, wordsInfer = self.getGFormat(configParas, gVeparas)
        fcCode = None
        for word in wordsInfer:
            if word[1] == 0:
                fcCode = word[0]
                break
        tFunMsgs = self.clsByFunc(fcCode)
        for fcKey in  tFunMsgs:
            tFunMsgs[fcKey] = self.getCFormat(configParas, gVeparas, tFunMsgs[fcKey])
        return wordsInfer, tFunMsgs
            #print(tFunMsgs[fcKey])

    def GTJsonTree(self, configParas, gVeparas):
        gFormat, cFormats = self.GTreeGenerate(configParas, gVeparas)
        print(gFormat)
        groot = self.icsSymTree.icsSymToTree(gFormat, cFormats)
        return groot.transToIcsDictTree()


    def changeFormat(self, boundaries, wordsType):
        boundaries = [boundaries for i in range(len(self.messages))]
        gForMsg = self.msgSplt.splitMsgByTypes(boundaries, self.messages)
        wordTHeaders = []
        for wordType in wordsType:
            wordTHeaders.append(self.wordTypeInfer.cVertNumToName(wordType[1]))
        return wordTHeaders, gForMsg

    def getGJson(self, congigParas, gVeparas):
        boundaries, wType = self.getGFormat(congigParas, gVeparas)
        return self.changeFormat(boundaries, wType)
        #print(boundaries)

    def getGF(self, uId=' '):
        # future
        uConfig = UserConfig('/home/wxw/data/ToolDatas/15895903730.10.222', '15895903730')
        gVeParas = GveConf.geneGveParas()
        return self.getGJson(uConfig, gVeParas)

    def combineFormats(self):
        pass

    def clsMessages(self):
        pass



