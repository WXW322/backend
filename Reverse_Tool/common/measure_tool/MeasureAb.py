from common.measure_tool.measure_base import Base_measure
from Data_base.Data_redis.redis_deal import redis_convert
from Config.ve_strategy import ve_strategy
from common.Converter.word_converter import word_convert

class MeasureAb(Base_measure):
    def __init__(self):
        super(MeasureAb,self).__init__()

    def MeasureDic(self, dicA, dicB):
        dicA = self.cvt(dicA)
        dicB = self.cvt(dicB)
        t_lo = True
        for key in dicA:
            if(key not in dicB or dicA[key] != dicB[key]):
                t_lo = False
                break
        return t_lo

    def cvt(self, dic):
        dics = {}
        for key in dic:
            dics[str(key)] = dic[key]
        return dics

    def MeasureDics(self, dicAs, dicBs):
        i = 0
        diffDic = []
        while(i < len(dicAs)):
            if not self.MeasureDic(dicAs[i], dicBs[i]) or not self.MeasureDic(dicBs[i], dicAs[i]):
                diffDic.append((dicAs[i], dicBs[i]))
            i = i + 1
        return diffDic

    def Measure(self, DataTure, DataPredict):
        return self.MeasureDic(DataTure, DataPredict)

    def MeasureTuple(self, tA, tB):
        if tA[0] == tB[0] and tA[1] == tB[1]:
            return True
        else:
            return False

    def MeasureTuples(self, tAs, tBs):
        result = []


if __name__ == '__main__':
    prefix = ve_strategy().GetWordsKeys('raw_words')
    Newprefix = ve_strategy().GetWordsKeys('RawWords')
    PrimModbus = redis_convert.read_from_redis(prefix)
    SecondModbus = redis_convert.read_from_redis(Newprefix)
    print(MeasureAb().MeasureDic(PrimModbus, SecondModbus))
    #PrimIec104 = redis_convert.read_from_redis('correct_raw_words')
    #prefix = ve_strategy().GetWordsKeys('RawWords')
    #NewIec104 = redis_convert.read_from_redis(prefix)
    #print(word_convert().splitwords_bylen(NewIec104, 5)[1])
    #print(MeasureAb().MeasureDic(PrimIec104, NewIec104))