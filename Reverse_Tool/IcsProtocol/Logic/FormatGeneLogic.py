
from IcsProtocol.Logic.GVoterLogic import GvoterLogic
from common.FieldTypeInfer.WholeFieldTypeInfer import WholeFieldTypeInfer
from Config.UserConfig import UserConfig
from IcsProtocol.Config.GveConf import GveConf
from common.FieldTypeInfer.WholeFieldTypeInfer import WholeFieldTypeInfer
from common.Converter.base_convert import Converter

class FormatGeneLogic:
    def __init__(self, messages):
        self.messages = messages
        self.wordTypeInfer = WholeFieldTypeInfer(self.messages)
        self.cvter = Converter()

    def getRanges(self, messages):
        L_len = 65536
        for message in messages:
            if len(message) < L_len:
                L_len = len(message)
        return min(23, L_len + 2)

    def getMesFormat(self):
        pass


    def getGFormat(self, congigParas, gVeparas):
        gVoterLogic = GvoterLogic()
        boundaries = gVoterLogic.getSplitMessages(congigParas, gVeparas, self.messages)
        boundaries = self.cvter.border2item(boundaries)
        fRange = self.getRanges(self.messages)
        wordsType = self.wordTypeInfer.extractWords(boundaries, fRange)
        print(wordsType)

    def combineFormats(self):
        pass

    def clsMessages(self):
        pass



