from netzob.all import *
from common.FieldTypeInfer.BaseFieldTypeInfer import BaseFieldTypeInfer
from common.Converter.base_convert import Converter
from common.analyzer.analyzer_common import base_analyzer
from common.readdata import *
import sys


class WholeFieldTypeInfer(BaseFieldTypeInfer):
    def __init__(self, messages=None):
        self.MaxLen = 40
        self.lengthThreshold = 0.8
        self.constThreshold = 0.98
        self.idThreshold = 0.7
        self.messages = messages
        self.cverter = Converter()


    def inferConst(self, Los=None, datas=None):
        if Los != None:
            datas = self.cverter.getDatasByLocs(self.messages, Los)
        wordDic = Converter.convert_raw_to_count(datas)
        wordDic = sorted(wordDic.items(), key=lambda x: x[1])
        if (wordDic[-1][1] / len(datas) > self.constThreshold):
            return 1
        else:
            return 0

    def inferSeriesId(self, Los=None, datas=None):
        if Los != None:
            datas = self.cverter.getDatasByLocs(self.messages, Los)
        ids = []
        for i, data in enumerate(datas):
            ids.append(i)
        datasBigInt = Converter.bytesToBigInt(datas)
        datasLittle = Converter.bytesToLittleInt(datas)
        tRate = max(base_analyzer.pearson(ids, datasBigInt), base_analyzer.pearson(ids, datasLittle))
        if (tRate > self.idThreshold):
            return 1
        else:
            return 0


    def inferLen(self, Los = None, datas = None):
        if Los != None:
            datas = self.cverter.getDatasByLocs(self.messages, Los)
        lens = [len(data) for data in datas]
        datasLenBig = Converter.bytesToBigInt(datas)
        datasLittle = Converter.bytesToLittleInt(datas)
        personBig = base_analyzer.pearson(datasLenBig, lens)
        personLittle = base_analyzer.pearson(datasLittle, lens)
        if personBig > self.lengthThreshold or personLittle > self.lengthThreshold:
            return 1
        else:
            return 0

    def inferLenAccau(self, Los = None, datas = None):
        if Los != None:
            datas = self.cverter.getDatasByLocs(self.messages, Los)
        lens = []
        for data in datas:
            if len(data) > Los[-1]:
                lens.append(len(data) - Los[-1])
            else:
                lens.append(-1)
        datasLenBig = Converter.bytesToBigInt(datas)
        datasLittle = Converter.bytesToLittleInt(datas)
        acc_big = 0
        for i in range(len(datasLenBig)):
            if (abs((datasLenBig[i] - lens[i])) <= 1):
                acc_big = acc_big + 1
        acc_small = 0
        for i in range(len(datasLittle)):
            if (abs((datasLittle[i] - lens[i])) <= 1):
                acc_small = acc_small + 1
        if ((acc_small / len(datas)) > self.lengthThreshold or (acc_big / len(datas)) > self.lengthThreshold):
            return 1
        else:
            return 0

    def getFuncScore(self, Los=None, datas = None):
        if Los != None:
            datas = self.cverter.getDatasByLocs(self.messages, Los)
        datasDic = Converter.convert_raw_to_count(datas)
        sumValue = 0
        for value in datasDic.values():
            sumValue = sumValue + value
        datas = [data/sumValue for data in datasDic.values()]
        datasEntry = base_analyzer.get_entry(datas)
        return datasEntry, len(datasDic)

    def inferFunc(self, tIdoms, T=0):
        t_max = -10000
        t_f = None
        t_es = []
        t_cs = []
        t_L = tIdoms[-1][1]
        t_E = -100
        t_C = -100
        T_f = []
        for t_idom in tIdoms:
            t_en, t_l = self.getFuncScore(t_idom)
            if t_E < t_en:
                t_E = t_en
            if t_C < t_l:
                t_C = t_l
            t_es.append(t_en)
            t_cs.append(t_l)
        t_E = t_E + 1
        t_C = t_C + 1
        i = 0
        while (i < len(tIdoms)):
            t_num = 1 - tIdoms[i][0] / t_L
            t_eum = 1 - t_es[i] / t_E
            t_cum = 1 - t_cs[i] / t_C
            print(tIdoms[i], t_num, t_eum, t_cum)
            t_fnum = t_num * t_eum * t_cum
            print(tIdoms[i], t_fnum)
            if (t_fnum > t_max):
                t_max = t_fnum
                t_f = tIdoms[i]
            if t_fnum > T:
                T_f.append(tIdoms[i])
            i = i + 1
        return t_f, T_f

    def get_loinfo(self, t_idom):
        if self.inferConst(t_idom) == 1:
            return 1
        elif self.inferLenAccau(t_idom) == 1:
            return 2
        elif self.inferSeriesId(t_idom) == 1:
            return 3
        else:
            return 4

    def extractWords(self, t_idoms, head):
        for t_idom in t_idoms:
            if t_idom[1] > head:
                t_idoms.remove(t_idom)
        t_words = {}
        for t_idom in t_idoms:
            if t_idom[1] == -1:
                t_words[t_idom] = 6
                continue
            t_info = self.get_loinfo(t_idom)
            if t_info != 4:
                t_words[t_idom] = t_info
        print(t_words)
        t_funcs = []
        for t_idom in t_idoms:
            if(t_idom not in t_words):
                t_funcs.append(t_idom)
        t_funw,T_f = self.inferFunc(t_funcs)
        t_words[t_funw] = 0
        for t_idom in t_idoms:
            if t_idom not in t_words:
                t_words[t_idom] = 6
        return t_words



if __name__ == '__main__':
    messages = read_datas('/home/wxw/data/ToolDatas/15895903730.10.222', 'single')
    messages = get_puredatas(messages)
    wholeFieldInfer = WholeFieldTypeInfer(messages)
    print(wholeFieldInfer.extractWords([(0, 2), (2, 5), (5, 7), (7, 8), (8, 9), (9, 11)], 12))





