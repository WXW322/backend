
from textops.TextParseLogic import TextParseLogic
from textops.TextClassifyLogic import TextClassifyLogic
from common.DataTuning.RawDataTuning.DataTuning import DataTuning
from textops.TextSympolToTree import TextSympolToTree
from Inferformat.node import node

class TextViewLogic:
    def __init__(self):
        self.dataTuning = DataTuning()
        self.textParser = TextParseLogic()

    def spltMsgs(self, msgs, maxRange=150):
        #msgs = self.dataTuning.textReadDatasTemp('')
        spltResults = self.textParser.spltMsgsSimple(msgs, b'\r\n', maxRange)
        return spltResults

    def formatInfer(self):
        #msgs = self.dataTuning.textReadDatasTemp('')
        msgs = self.dataTuning.readDatasByType('textPro')
        message_parser = TextParseLogic()
        srcmessages = message_parser.ConvertDataToMessage(msgs, b'\r\n', h=2)
        # future
        #textCls = TextClassifyLogic(srcmessages, 0.05, 0.2, 0.2, 3)
        textCls = TextClassifyLogic(srcmessages, 0.1, 0.2, 0.2, 3)
        formats = textCls.formatInfer(srcmessages)
        nodeRoot = node(wType='root')
        textSymTree = TextSympolToTree()
        for f in formats:
            nodeT = textSymTree.subSymbolToTree(f)
            nodeRoot.children.append(nodeT)
        return nodeRoot.transToDictTree()


