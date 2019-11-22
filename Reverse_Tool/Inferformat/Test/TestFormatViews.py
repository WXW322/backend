

from BinaryProtocol.Logic.MsgSplitLogic import MegSplitLogic
from Inferformat.FormatViews import getFormat
from common.readdata import *
from common.Model.PrimData import primeData
from Inferformat.treef import treef
from Inferformat.treeFormat import treeFormat
from common.DataTuning.RawDataTuning.FTPDataTuning import FTPDataTuning

class FormatViewTest:
    def __init__(self):
        self.msg = MegSplitLogic()

    def geneDatas(self):
        messages = read_datas('/home/wxw/data/modbusdata', 'single')
        messages = get_puredatas(messages)[0:1000]
        return messages

    def geneDatas(self):
        pass

    def testModData(self):
        #datas = self.geneDatas()
        srcDatas, desDatas = FTPDataTuning().tuningHttpByregix()
        datas = []
        datas.extend(srcDatas)
        datas.extend(desDatas)
        vePara = {'diffMeasure': 'abs', 'vWayFre': 'loose', 'T': 0, 'r': 0.3}
        borders = self.msg.getFreBorders(vePara, datas)
        i = 0
        primDatas = []
        print(datas[0])
        while(i < len(datas)):
            primDatas.append(primeData(datas[i], borders[i], i))
            i = i + 1
        tree_builder = treeFormat(primDatas, 20, 0.2)
        t_result = tree_builder.generateNT()
        t_result.depth_traverse()
        for f in t_result.result:
            print("format start")
            for node_i in f:
                print(node_i.loc, node_i.word_type, node_i.value)
                #print(node_i.getNodeData())

    def testModDataOne(self):
        # datas = self.geneDatas()
        srcDatas, desDatas = FTPDataTuning().tuningHttpByregix()
        datas = []
        datas.extend(srcDatas)
        datas.extend(desDatas)
        vePara = {'diffMeasure': 'abs', 'vWayFre': 'loose', 'T': 0, 'r': 0.3}
        borders = self.msg.getFreBorders(vePara, datas)
        i = 0
        primDatas = []
        print(datas[0])
        while (i < len(datas)):
            primDatas.append(primeData(datas[i], borders[i], i))
            i = i + 1
        tree_builder = treeFormat(primDatas, 10, 0.2)
        #t_result = tree_builder.generateNT()
        t_result = tree_builder.generateSplitNT()
        t_result.showTree(0)
        #tree_builder.layyerTree()


if __name__ == '__main__':
    fTest = FormatViewTest()
    fTest.testModDataOne()
    #fTest.testModData()