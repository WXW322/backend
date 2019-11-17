
from common.Spliter.vertical_splitter import vertical_splitter
from common.Merger.base_merger import base_merger
from Inferformat.node import node
from common.FieldTypeInfer.WholeFieldTypeInfer import WholeFieldTypeInfer

class ReAjustLogic:
    def __init__(self):
        pass

    def reAjustBorders(self, words, messages):
        vSpliter = vertical_splitter(messages)
        words = vSpliter.splitWordsSimple(words)
        Nodes = []
        typeInfer = WholeFieldTypeInfer(messages)
        mgerItoms = base_merger()
        for word in words:
            if typeInfer.inferConst(word):
                tNode = node(loc=word, wType=1)
            else:
                tNode = node(loc=word, wType=6)
            Nodes.append(tNode)
        return mgerItoms.merge_words(Nodes)



