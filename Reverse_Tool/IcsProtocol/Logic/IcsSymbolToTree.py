from Inferformat.node import node
from common.FieldTypeInfer.WholeFieldTypeInfer import WholeFieldTypeInfer



class IcsSymbolToTree:
    def __init__(self):
        self.wTInfer = WholeFieldTypeInfer()

    def icsSymToTree(self, gFormat, cFormats, h=10):
        gNodeFirst, gNodeLast = self.transLineToNodes(gFormat[0:len(gFormat)-1])
        for cFormat in cFormats:
            tFuncNode = node()
            tType = 'F' + ',' + str(len(cFormat)) + ',' + str(cFormat)
            tFuncNode.value.append(tType)
            tCformat,_ = self.transLineToNodes(cFormats[cFormat], h=3)
            tFuncNode.children.append(tCformat)
            gNodeLast.children.append(tFuncNode)
        return gNodeFirst

    def transLineToNodes(self, words, h=10):
        nodes = []
        for word in words:
            wType = self.wTInfer.cVertNumToName(word[1])
            sNode = ''
            if wType == 'Payload':
                sNode = sNode + wType + ',' + '-1'
            else:
                sNode = sNode + wType + ',' + str(word[0][1] - word[0][0])
            tNode = node()
            tNode.value.append(sNode)
            nodes.append(tNode)
        t_len = min(len(words), h)
        i = t_len - 2
        while(i >= 0):
            nodes[i].children.append(nodes[i+1])
            i = i - 1
        return nodes[0], nodes[t_len-1]

