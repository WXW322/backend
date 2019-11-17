from common.readdata import *
from common.Merger.base_merger import base_merger
from protocol_analysis.word_simple import word_infer
from Fields_info.const_field import loc_field
from common.Converter.base_convert import Converter
from common.analyzer.analyzer_common import base_analyzer
import sys
from common.FieldTypeInfer.WholeFieldTypeInfer import WholeFieldTypeInfer

class vertical_splitter:
    def __init__(self, messages):
        self.messages = messages
        self.wholeFieldInfer= WholeFieldTypeInfer(self.messages)

    def split_by_words_type(self, datas, T_max_range):
        fields_set = []
        w_infer = word_infer()
        w_merger = base_merger()
        w_convert = Converter()
        b_analyzer = base_analyzer()
        for i in range(T_max_range):
            lo_datas = get_data_bylo(datas, i)
            w_cnt = w_convert.convert_raw_to_count(lo_datas)
            w_frequent = b_analyzer.convert_num_to_frequent(w_cnt)
            w_type = w_infer.is_const_word(w_frequent, 0.95)
            if w_type:
                t_field = loc_field((i,i), 0)
            else:
                t_field = loc_field((i,i), 4)
            fields_set.append(t_field)
        words_f = w_merger.merge_words(fields_set)
        candidate_borders = [w.loc[0] for w in words_f]
        return words_f, candidate_borders

    def splitWordSimple(self, word):
        if word[1] - word[0] == 1:
            return word, None
        else:
            j = word[0] + 1
            tLo = -1
            while(j < word[1]):
                if (self.wholeFieldInfer.inferConst((word[0], j)) \
                    and not self.wholeFieldInfer.inferConst((j, word[1]))) \
                    or (self.wholeFieldInfer.inferConst((j, word[1])) and \
                        not self.wholeFieldInfer.inferConst((word[0], j))):
                    tLo = j
                j = j + 1
            wA = (word[0], tLo)
            wB = (tLo, word[1])
            if tLo != -1:
                return wA, wB
            else:
                return word, None

    def splitWordsSimple(self, words):
        i = 0
        while(i < len(words)):
            self.splitWordSimple(words[i])
            wOne, wTwo = self.splitWordSimple(words[i])
            if wTwo != None:
                words.remove(words[i])
                words.append(wOne)
                words.append(wTwo)
            words = sorted(words, key = lambda x:x[0])
            i = i + 1
        return words

if __name__ == '__main__':
    ver_split = vertical_splitter()
    datas = read_multity_dirs(["/home/wxw/data/modbusdata", "/home/wxw/data/modbus_github"])
    datas = get_puredatas(datas)
    w_result, borders = ver_split.split_by_words_type(datas, 15)
    for w in w_result:
        print(w.loc, w.word_type)
    print(borders)




