from Config.UserConfig import UserConfig
from ngrambuild.pyngram import voters

def TestWords():
    UserConfig.userId = '15895903730'
    UserConfig.path = '/home/wxw/data/ToolDatas/15895903730.10.222'
    Voter = voters()
    print(Voter.getQueryWords(UserConfig.getUserPath()))

def TestFreWords():
    UserConfig.userId = '15895903730'
    UserConfig.path = '/home/wxw/data/ToolDatas/15895903730.10.222'
    Voter = voters()
    print(Voter.getQueryFrequentWords(UserConfig.getUserPath()))

def TestEntryWords():
    UserConfig.userId = '15895903730'
    UserConfig.path = '/home/wxw/data/ToolDatas/15895903730.10.222'
    Voter = voters()
    print(Voter.getQueryEntryWords(UserConfig.getUserPath()))

if __name__ == '__main__':
    #TestWords()
    #TestFreWords()
    TestEntryWords()

