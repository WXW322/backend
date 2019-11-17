
from IcsProtocol.Logic.GVoterLogic import GvoterLogic
from Config.UserConfig import UserConfig
from IcsProtocol.Config.GveConf import GveConf
from common.readdata import *

def testForGVotes():
    uConfig = UserConfig('/home/wxw/data/ToolDatas/15895903730.10.222', '15895903730')
    messages = read_datas('/home/wxw/data/ToolDatas/15895903730.10.222', 'single')
    messages = get_puredatas(messages)
    gVoterLogic = GvoterLogic()
    print(gVoterLogic.getGVotes(uConfig, messages))

def testForGetBouns():
    uConfig = UserConfig('/home/wxw/data/ToolDatas/15895903730.10.222', '15895903730')
    messages = read_datas('/home/wxw/data/ToolDatas/15895903730.10.222', 'single')
    messages = get_puredatas(messages)
    gVeParas = GveConf.geneGveParas()
    gVoterLogic = GvoterLogic()
    print(gVoterLogic.getBoundaries(uConfig, gVeParas, messages))

def testForSplitMsgs():
    uConfig = UserConfig('/home/wxw/data/ToolDatas/15895903730.10.222', '15895903730')
    messages = read_datas('/home/wxw/data/ToolDatas/15895903730.10.222', 'single')
    messages = get_puredatas(messages)
    gVeParas = GveConf.geneGveParas()
    gVoterLogic = GvoterLogic()
    print(gVoterLogic.splitMessages(uConfig, gVeParas, messages))

if __name__ == '__main__':
    #testForGVotes()
    testForGetBouns()
    #testForSplitMsgs()