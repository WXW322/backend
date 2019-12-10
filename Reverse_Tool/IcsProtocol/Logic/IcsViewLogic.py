
from IcsProtocol.Logic.GVoterLogic import GvoterLogic
from Config.UserConfig import UserConfig
from IcsProtocol.Config.GveConf import GveConf


class IcsViewLogic:
    def __init__(self):
        pass

    def getSplitMsgs(self, msgs, maxRange=15):
        gVeParas = GveConf.geneGveParas()
        uConfig = UserConfig('/home/wxw/data/ToolDatas/15895903730.10.222', '15895903730')
        gVoterLogic = GvoterLogic()
        return gVoterLogic.splitMessages(uConfig, gVeParas, msgs, maxRange)
