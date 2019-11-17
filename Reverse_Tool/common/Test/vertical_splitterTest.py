
from common.Spliter.vertical_splitter import vertical_splitter
from common.readdata import *

class vertical_splitterTest:
    def __init__(self, messages):
        self.vertical = vertical_splitter(messages)

    def testVerticalSplit(self):
        print(self.vertical.splitWordsSimple([(3, 5), (5, 7)]))

if __name__ == '__main__':
    messages = read_datas('/home/wxw/data/ToolDatas/15895903730.10.222', 'single')
    messages = get_puredatas(messages)
    sptTest = vertical_splitterTest(messages)
    print(sptTest.testVerticalSplit())

