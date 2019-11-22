
from netzob.all import *
from common.FieldTypeInfer.BaseFieldTypeInfer import BaseFieldTypeInfer
from common.Converter.base_convert import Converter
from common.analyzer.analyzer_common import base_analyzer

class LocalFieldTypeInfer(BaseFieldTypeInfer):
    def __init__(self, FuncT = 22):
        self.constThreshold = 0.98
        self.FuncT = FuncT
        self.lengthThreshold = 0.8


    def inferConst(self, datas):
        wordDic = Converter.convert_raw_to_count(datas)
        wordDic = sorted(wordDic.items(), key=lambda x: x[1])
        if (wordDic[-1][1] / len(datas) > self.constThreshold):
            return 1
        else:
            return 0

    def inferSeriesId(self):
        pass

    def inferLen(self, datas, lenDatas):
        datasLenBig = Converter.bytesToBigInt(datas)
        datasLittle = Converter.bytesToLittleInt(datas)
        personBig = base_analyzer.pearson(datasLenBig, lenDatas)
        personLittle = base_analyzer.pearson(datasLittle, lenDatas)
        if personBig > self.lengthThreshold or personLittle > self.lengthThreshold:
            return 1
        else:
            return 0

    def inferFunc(self, datas):
        datasDic = Converter.convert_raw_to_count(datas)
        sumValue = 0
        for value in datasDic.values():
            sumValue = sumValue + value
        datas = [data/sumValue for data in datasDic.values()]
        datasEntry = base_analyzer.get_entry(datas)
        if len(datasDic) < self.FuncT:
            return 1
        else:
            return 0
