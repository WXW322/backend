
from netzob.all import *
from Inferformat.node import node
import sys
from showresult.graph_build import tree_graph

class TextSympolToTree:
    def __init__(self):
        self.Tgraph = tree_graph('a', 'B')

    def symbolToTree(self, symbolOne):
        nodeRoot = node(wType='root')
        nodeRoot.children = self.getSubTree(symbolOne.fields)
        return nodeRoot

    def subSymbolToTree(self, symbolTwo):
        return self.colToLineTree(self.getsubTreeTwo(symbolTwo.fields))
        #return self.colToLineTree(self.getSubTree(symbolTwo.fields))

    def symbolsToTree(self, formats, path):
        nodeRoot = node(wType='root')
        for f in formats:
            nodeT = self.subSymbolToTree(f)
            nodeRoot.children.append(nodeT)
        nodeRoot.showTree(0)
        self.Tgraph.graph_buildFour(nodeRoot, path)

    def getSubTree(self, fields):
        tNodes = []
        for field in fields:
            if field.domain.currentValue != None:
                tValue = field.domain.currentValue.tobytes()
                tNode = node(wType='C')
                tNode.value.append('CRLF'.join([str(v) for v in tValue.split(b'\r\n')]))
                leafs = field.getLeafFields(1)
                if len(leafs) > 0 and leafs[0] != field:
                    tNode.children = self.getSubTree(leafs)
                tNodes.append(tNode)
            else:
                tNode = node(wType='V')
                leafs = field.getLeafFields(1)
                if len(leafs) > 0 and leafs[0] != field:
                    tNode.children = self.getSubTree(leafs)
                tNodes.append(tNode)
        return tNodes

    def getsubTreeTwo(self, fields):
        tNodes = []
        for field in fields:
            if field.domain.currentValue != None:
                tValue = field.domain.currentValue.tobytes()
                if tValue.find(b'\r\n' != -1):
                    splitDatas = tValue.split(b'\r\n')
                    tLen = len(splitDatas)
                    i = 0
                    while i < tLen - 2:
                        tNode = node(wType='C')
                        tNode.value.append(splitDatas[i])
                        tNodes.append(tNode)
                        tNode = node(wType='C')
                        tNode.value.append('CRLF')
                        tNodes.append(tNode)
                        i = i + 1
                    tNode = node(wType='C')
                    tNode.value.append(splitDatas[i])
                    tNodes.append(tNode)
                    if tValue[-2:] == b'\r\n':
                        tNode = node(wType='C')
                        tNode.value.append('CRLF')
                        tNodes.append(tNode)
                else:
                    tNode = node(wType='C')
                    tNode.value.append(tValue)
                    tNodes.append(tNode)
                leafs = field.getLeafFields(1)
                if len(leafs) > 0 and leafs[0] != field:
                    tNode.children = self.getSubTree(leafs)
                #tNodes.append(tNode)
            else:
                tNode = node(wType='V')
                leafs = field.getLeafFields(1)
                if len(leafs) > 0 and leafs[0] != field:
                    tNode.children = self.getSubTree(leafs)
                tNodes.append(tNode)
        return tNodes


    def colToLineTree(self, colNodes):
        tLen = len(colNodes)
        #i = tLen - 2
        i = 4
        while(i >= 0):
            colNodes[i].children.append(colNodes[i+1])
            i = i - 1
        return colNodes[0]





