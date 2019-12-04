
from CompareStudies.TextTools.TextClassify import TextClassify
from common.DataTuning.RawDataTuning.HttpDataTuning import HttpDataTuning
from common.DataTuning.RawDataTuning.FTPDataTuning import FTPDataTuning
from common.DataTuning.RawDataTuning.RedisDataTuning import RedisDataTuning
from netzob.all import *

class TextFormInfer:
    def __init__(self, messages):
        self.clser = TextClassify(messages)
        self.httptuning = HttpDataTuning()
        self.ftptuning = FTPDataTuning()
        self.redistuning = RedisDataTuning()

    def ldaFormatInfer(self, wSize, TK, wLen, Kcls, infercls = 'H'):
        clsDatas = self.clser.clsMessages(wSize, TK, wLen, Kcls)
        clsFormats = []
        formatInfer = Format()
        clusters = [cluster for cluster in clsDatas.values()]
        if infercls == 'H':
            self.httptuning.getMsgsLen(clusters)
        elif infercls == 'F':
            self.ftptuning.getMsgsLen(clusters)
        else:
            self.redistuning.getMsgsLen(clusters)
        for clsData in clsDatas.values():
            tMessages = [RawMessage(message) for message in clsData]
            tempFormat = Symbol(messages=tMessages)
            formatInfer.splitAligned(tempFormat, doInternalSlick=True)
            clsFormats.append(tempFormat)
        return clsFormats

    def ladDbscanFormatInfer(self, wSize, TK, wLen, mindis, minpt, infercls):
        clsDatas = self.clser.clsByDbscan(wSize, TK, wLen, mindis, minpt)
        clusters = [cluster for cluster in clsDatas.values()]
        if infercls == 'H':
            self.httptuning.getMsgsLen(clusters)
        elif infercls == 'F':
            self.ftptuning.getMsgsLen(clusters)
        else:
            self.redistuning.getMsgsLen(clusters)
        clsFormats = []
        formatInfer = Format()
        for clsData in clsDatas.values():
            tMessages = [RawMessage(message) for message in clsData]
            tempFormat = Symbol(messages=tMessages)
            formatInfer.splitAligned(tempFormat, doInternalSlick=True)
            clsFormats.append(tempFormat)
        return clsFormats



