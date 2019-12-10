# -*- coding: utf-8 -*-
from BinaryProtocol.Logic.MsgSplitLogic import MegSplitLogic
from Inferformat.FormatViews import getFormat
from common.DataTuning.RawDataTuning.DataTuning import DataTuning
from common.Model.PrimData import primeData
from Inferformat.treef import treef
from Inferformat.treeFormat import treeFormat
from showresult.graph_build import tree_graph
from BinaryProtocol.Logic.MsgSplitLogic import MegSplitLogic
import sys

class MsgForMatG:
    def __init__(self):
        self.dataTuning = DataTuning()
        self.msgSplit = MegSplitLogic()

    def transRawDataToPrim(self, datas, borders):
        primDatas = []
        i = 0
        while (i < len(datas)):
            primDatas.append(primeData(datas[i], borders[i], i))
            i = i + 1
        return primDatas



    def generateTree(self, primDatas, treeParas):
        height = treeParas['h']
        funNum = treeParas['fcNum']
        splitRate = treeParas['srate']
        tree_builder = treeFormat(primDatas, funNum, splitRate)
        t_result = tree_builder.generateSplitNT(height)
        t_json = t_result.transToDictTree()
        return t_json

    def msgToTree(self, filePath='', datas=None):
        borders= None
        datas = None
        if filePath != '':
            #datas = self.dataTuning.readDatasTemp(filePath)
            datas = self.dataTuning.readDatasByType('binaryPro')
        if filePath != '':
            borders,_ = self.msgSplit.getOrderBordersNyPath(filePath, datas)
        primDatas = self.transRawDataToPrim(datas, borders)
        #可替换函数
        treeParas = {'h': 5, 'fcNum': 20, 'srate': 0.2}
        treeJson = self.generateTree(primDatas, treeParas)
        return treeJson

if __name__ == '__main__':
    msgF = MsgForMatG()
    print(msgF.msgToTree(filePath='aaa'))

