from sklearn.feature_extraction.text import CountVectorizer
import re
from common.readdata import *
from common.Converter.base_convert import Converter
from sklearn.feature_extraction.text import TfidfTransformer
from common.analyzer.analyzer_common import base_analyzer
from common.ranker import ranker
from common.DataTuning.RawDataTuning.HttpDataTuning import HttpDataTuning

class FieldHunter:
    def __init__(self):
        self.analyer = base_analyzer()
        self.convert = Converter()
        self.ranker = ranker()

    def itemJudge(self, item):
        if int(item) >= 48 and int(item) <= 57:
            return True
        if int(item) >= 65 and int(item) <= 90:
            return True
        if int(item) >= 97 and int(item) <= 122:
            return True
        return False

    def isNumOrAlpha(self, sequence):
        chars = sequence.split(' ')
        isNumAlpha = False
        for item in chars:
            if self.itemJudge(item):
                isNumAlpha = True
                break
        return isNumAlpha

    def findDelimiter(self, messages):
        messages = [self.convert.convert_raw_to_text(data) for data in messages]
        wordsNgram = self.convert.ConvertRawToSimDic(messages, (1, 2))
        wordsNgram = self.ranker.rank_dic(wordsNgram, reverse=True)
        #print(wordsNgram)
        delimiter = None
        for word in wordsNgram:
            if not self.isNumOrAlpha(word[0]):
                delimiter = word
                break
        candidates = []
        for word in wordsNgram:
            if not self.isNumOrAlpha(word[0]):
                candidates.append(word[0])
        print(candidates)
        return delimiter


if __name__ == '__main__':
    ff = FieldHunter()
    #datas = read_datas('/home/wxw/data/httpDatas/http_test', 'single')
    #datas = get_puredatas(datas)
    httpDatatuning = HttpDataTuning()
    src, des = httpDatatuning.tuningHttpByregix()
    datas = []
    datas.extend(src)
    datas.extend(des)
    print(ff.findDelimiter(datas))