from  IcsProtocol.Logic.FormatGeneLogic import FormatGeneLogic
from Config.UserConfig import UserConfig
from IcsProtocol.Config.GveConf import GveConf
from common.readdata import *

class FormatGeneLogicTest:
    def __init__(self, messages):
        self.formatLogic = FormatGeneLogic(messages)

    def testFormatGene(self, configParas, gVeparas):
        print(self.formatLogic.getGFormat(configParas, gVeparas))

    def testForJson(self, configParas, gVeparas):
        print(self.formatLogic.getGJson(configParas, gVeparas))

    def testForGF(self):
        print(self.formatLogic.getGF())

    def testGtree(self, configParas, gVeparas):
        print(self.formatLogic.GTreeGenerate(configParas, gVeparas))

    def testGJsonTree(self, configParas, gVeparas):
        print(self.formatLogic.GTJsonTree(configParas, gVeparas))


if __name__ == '__main__':
    uConfig = UserConfig('/home/wxw/data/ToolDatas/15895903730.10.222', '15895903730')
    messages = read_datas('/home/wxw/data/ToolDatas/15895903730.10.222', 'single')
    messages = get_puredatas(messages)
    gVeParas = GveConf.geneGveParas()
    formatGene = FormatGeneLogicTest(messages)
    formatGene.testGJsonTree(uConfig, gVeParas)
    #formatGene.testGtree(uConfig, gVeParas)
    #formatGene.testForGF()

    #formatGene.testForJson(uConfig, gVeParas)
    #formatGene.testFormatGene(uConfig, gVeParas)

