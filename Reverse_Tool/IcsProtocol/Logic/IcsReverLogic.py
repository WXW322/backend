
from IcsProtocol.Logic.FormatGeneLogic import FormatGeneLogic
from common.DataTuning.RawDataTuning.DataTuning import DataTuning
from Config.UserConfig import UserConfig
from IcsProtocol.Config.GveConf import GveConf
from IcsProtocol.Logic.GVoterLogic import GvoterLogic


class IcsReverLogic:
    def __init__(self):
        self.dataTuning = DataTuning()

    def getIcsTree(self):
        messages = self.dataTuning.readDatasByType('icsPro')
        uConfig = UserConfig('/home/wxw/data/ToolDatas/15895903730.10.222', '15895903730')
        gVeParas = GveConf.geneGveParas()
        formatGene = FormatGeneLogic(messages)
        return formatGene.GTJsonTree(uConfig, gVeParas)

    def getSplitMsgs(self, msgs, maxRange=15):
        gVeParas = GveConf.geneGveParas()
        uConfig = UserConfig('/home/wxw/data/ToolDatas/15895903730.10.222', '15895903730')
        gVoterLogic = GvoterLogic()
        return gVoterLogic.splitMessages(uConfig, gVeParas, msgs, maxRange)