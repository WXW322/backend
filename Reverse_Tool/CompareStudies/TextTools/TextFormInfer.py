
from CompareStudies.TextTools.TextClassify import TextClassify
from netzob.all import *

class TextFormInfer:
    def __init__(self, messages):
        self.clser = TextClassify(messages)

    def ldaFormatInfer(self, wSize, TK, wLen, Kcls):
        clsDatas = self.clser.clsMessages(wSize, TK, wLen, Kcls)
        clsFormats = []
        formatInfer = Format()
        for clsData in clsDatas.values():
            tMessages = [RawMessage(message) for message in clsData]
            tempFormat = Symbol(messages=tMessages)
            formatInfer.splitAligned(tempFormat, doInternalSlick=True)
            clsFormats.append(tempFormat)
        return clsFormats



