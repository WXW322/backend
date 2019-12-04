

from BinaryProtocol.Logic.MsgSplitLogic import MegSplitLogic
from Inferformat.FormatViews import getFormat
from common.readdata import *
from common.Model.PrimData import primeData
from Inferformat.treef import treef
from Inferformat.treeFormat import treeFormat
from common.DataTuning.RawDataTuning.FTPDataTuning import FTPDataTuning
from showresult.graph_build import tree_graph
from common.DataTuning.RawDataTuning.ModBusDataTuning import ModBusDataTuning
import sys

class FormatViewTest:
    def __init__(self):
        self.msg = MegSplitLogic()
        self.TGraph = tree_graph('a', 'B')
        self.moddatas = ModBusDataTuning()
        self.ftp = FTPDataTuning()

    def geneDatas(self):
        messages = read_datas('/home/wxw/data/modbusdata', 'single')
        messages = get_puredatas(messages)[0:1000]
        return messages

    def getMixDatas(self):
        MergeDatas = []
        modDatas = self.moddatas.getModDatas()
        ftpDatas = self.ftp.getTotalData()
        MergeDatas.extend(modDatas)
        MergeDatas.extend(ftpDatas)
        return MergeDatas

    def testModData(self):
        datas = self.geneDatas()
        vePara = {'diffMeasure': 'abs', 'vWayFre': 'loose', 'T': 0, 'r': 0.3}
        #borders = self.msg.getFreBorders(vePara, datas)
        borders = self.msg.getOrderBorders(vePara, datas)
        i = 0
        primDatas = []
        print(datas[0])
        while (i < len(datas)):
            primDatas.append(primeData(datas[i], borders[i], i))
            i = i + 1
        tree_builder = treeFormat(primDatas, 20, 0.2)
        # t_result = tree_builder.generateNT()
        t_result = tree_builder.generateSplitNT(5)
        Nodes = []
        Edges = []
        t_result.showTree(0)
        t_result.getGraph(0, Nodes, Edges, [0])
        self.TGraph.graph_buildTwo(Nodes, Edges, '/home/wxw/paper/researchresult/BinaryFormat/treeshow/Modbus Order 10 20.png')

    def testFTPData(self):
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

    def testFTPDataOne(self):
        # datas = self.geneDatas()
        srcDatas, desDatas = FTPDataTuning().tuningHttpByregix()
        datas = []
        datas.extend(srcDatas)
        datas.extend(desDatas)
        vePara = {'diffMeasure': 'abs', 'vWayFre': 'loose', 'T': 0, 'r': 0.3}
        borders = self.msg.getFreBorders(vePara, datas)
        #borders = self.msg.getOrderBorders(vePara, datas)
        i = 0
        primDatas = []
        print(datas[0])
        while (i < len(datas)):
            primDatas.append(primeData(datas[i], borders[i], i))
            i = i + 1
        tree_builder = treeFormat(primDatas, 10, 0.2)
        #t_result = tree_builder.generateNT()
        t_result = tree_builder.generateSplitNT(5)
        Nodes = []
        Edges = []
        t_result.showTree(0)
        t_result.getGraph(0, Nodes, Edges, [0])
        self.TGraph.graph_buildTwo(Nodes, Edges, '/home/wxw/paper/researchresult/BinaryFormat/treeshow/Fre 5 20.png')
        #t_result.showTree(0)
        #tree_builder.layyerTree()

    def testMixData(self):
        datas = self.getMixDatas()
        vePara = {'diffMeasure': 'abs', 'vWayFre': 'loose', 'T': 0, 'r': 0.3}
        #borders = self.msg.getFreBorders(vePara, datas)
        borders = self.msg.getOrderBorders(vePara, datas)
        i = 0
        primDatas = []
        print(datas[0])
        while (i < len(datas)):
            primDatas.append(primeData(datas[i], borders[i], i))
            i = i + 1
        tree_builder = treeFormat(primDatas, 10, 0.2)
        # t_result = tree_builder.generateNT()
        t_result = tree_builder.generateSplitNT(5)
        Nodes = []
        Edges = []
        t_result.showTree(0)
        t_result.getGraph(0, Nodes, Edges, [0])
        self.TGraph.graph_buildTwo(Nodes, Edges, '/home/wxw/paper/researchresult/BinaryFormat/treeshow/Order 5 20 10 MixData.png')


    def testMixTree(self):
        datas = self.getMixDatas()
        vePara = {'diffMeasure': 'abs', 'vWayFre': 'loose', 'T': 0, 'r': 0.3}
        # borders = self.msg.getFreBorders(vePara, datas)
        borders = self.msg.getOrderBorders(vePara, datas)
        i = 0
        primDatas = []
        print(datas[0])
        while (i < len(datas)):
            primDatas.append(primeData(datas[i], borders[i], i))
            i = i + 1
        tree_builder = treeFormat(primDatas, 10, 0.2)
        # t_result = tree_builder.generateNT()
        t_result = tree_builder.generateSplitNT(5)
        print(t_result.transToDictTree())


if __name__ == '__main__':
    fTest = FormatViewTest()
    fTest.testMixTree()
    #fTest.testMixData()
    #fTest.testFTPDataOne()
    #fTest.testModData()
    #fTest.testModData()