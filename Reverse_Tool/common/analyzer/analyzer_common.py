from Data_base.Data_redis.redis_deal import redis_deal
import numpy as np
import sys
from sklearn.feature_extraction.text import CountVectorizer
import math

redis_read = redis_deal()
class base_analyzer:
    def __init__(self):
        pass

    def rank_words(self, raw_words, max_num, top, reverse=True):
        t_dic = {}
        t_dic[1] = []
        t_dic[2] = []
        t_dic[3] = []
        t_dic[4] = []
        t_dic[5] = []
        for word in raw_words:
            t_dic[len(word.split(' '))].append((word, raw_words[word]))
        for i in range(1, 5):
            t_dic[i] = sorted(t_dic[i], key = lambda key: key[1], reverse=reverse)
            print(len(t_dic[i]))
        t_result = {}
        for i in range(1, 5):
            t_result[i] = t_dic[i][0:top]
            t_last_items = [item[1] for item in t_dic[i][top:]]
            t_result[i].append(('left', sum(t_last_items)))
        return t_result

    def get_ith_word(self, t_words, word):
        t_candidate_words = t_words[len(word.split(' '))]
        i = 0
        for c_word in t_candidate_words:
            if(word == c_word):
                break
            i = i + 1

    def convert_num_to_frequent(self, words_num_dic):
        t_count = 0
        words_frequent = {}
        for value in words_num_dic.values():
            t_count = t_count + value
        for key in words_num_dic:
            words_frequent[key] = words_num_dic[key] / t_count
        tValue = 0
        return words_frequent

    def get_topk(self, elements):
        t_result = {}
        for elem in elements:
            if elem not in t_result:
                t_result[elem] = 1
            else:
                t_result[elem] = t_result[elem] + 1
        t_result = sorted(t_result.items(), key = lambda key:key[1], reverse=True)
        return t_result

    @staticmethod
    def get_entry(t_datas):
        r_entry = 0
        for data in t_datas:
            r_entry = r_entry + data * np.log2(data)
        return -r_entry

    def get_manuation(self, fre_X, fre_Y, fre_Com):
        entry_X = self.get_enrty(fre_X)
        entry_Y = self.get_enrty(fre_Y)
        entry_com = self.get_enrty(fre_Com)
        return entry_X + entry_Y - entry_com

    def filter_words(self, words_dic, T):
        words_dic = filter(lambda x: x[1] > T, words_dic)
        return list(words_dic)


    def cls_diff_measure(self, A_set, B_set):
        return len(A_set & B_set) / min(len(A_set), len(B_set))

    def get_f1(self, DataPredict, DataRight):
        t_H = DataRight[-1]
        conpbors = set(DataPredict)
        rpborders = set(DataRight)
        T_boders = set([i for i in range(t_H + 1)])
        rnborders = T_boders - rpborders
        connbors = T_boders - conpbors
        tpborders = rpborders&conpbors
        fnborders = rpborders&connbors
        fpborders = rnborders&conpbors
        tnborders = rnborders&connbors
        acc = (len(tpborders) + len(tnborders))/(len(tpborders) + len(tnborders) + len(fnborders) + len(fnborders))
        pre = len(tpborders)/(len(tpborders) + len(fpborders))
        recall = (len(tpborders)/(len(tpborders) + len(fnborders)))
        f1 = 0
        if pre + recall != 0:
            f1 = 2*pre*recall/(pre + recall)
        return (pre,recall,f1)

    @staticmethod
    def pearson(vector1, vector2):
        n = len(vector1)
        # simple sums
        sum1 = sum(float(vector1[i]) for i in range(n))
        sum2 = sum(float(vector2[i]) for i in range(n))
        # sum up the squares
        sum1_pow = sum([pow(v, 2.0) for v in vector1])
        sum2_pow = sum([pow(v, 2.0) for v in vector2])
        # sum up the products
        p_sum = sum([vector1[i] * vector2[i] for i in range(n)])
        # 分子num，分母den
        num = p_sum - (sum1 * sum2 / n)
        den = math.sqrt((sum1_pow - pow(sum1, 2) / n) * (sum2_pow - pow(sum2, 2) / n))
        if den == 0:
            return 0.0
        return num / den

    @staticmethod
    def getSetDis(setA, setB):
        return len(setA & setB) / len(setA | setB)












if __name__ == '__main__':

    sA = {1, 2, 3}
    sB = {1, 2, 4}
    print(base_analyzer.getSetDis(sA, sB))
    '''
    analyzer = base_analyzer()
    sentence = ['1 2 1 2 3']
    vec = CountVectorizer(min_df=1, ngram_range=(1,2), stop_words=[' ','.'],token_pattern='(?u)\\b\\w\\w*\\b')
    x = vec.fit_transform(sentence)
    print(vec.get_feature_names())
    print(x.toarray())
    '''
    #words_normal = redis_read.read_from_redis('modbus_frequent_voter_abs_normal_0_0normal_correct_words')
    #analyzer.vote_item(['0', '83', '255', '4'], words_normal)
    #words_normal = redis_read.read_from_redis('modbus_frequent_voter_abs_normal_0_0correct_raw_words')
    #t_result = analyzer.rank_words(words_normal, 1, 100, False)
    #print(t_result)
    #print(analyzer.get_manuation([0.5, 0.5], [0.5, 0.5], [0.25, 0.25, 0.25, 0.25]))
    #t_results = analyzer.rank_words('correct_raw_words', 1, 1000)
    # analyzer.get_ith_word(t_results, '104')
    # analyzer.get_ith_word(t_results, '104 90')
    #analyzer.rank_words('raw_words', 1, 100)
    #analyzer.get_frequent("normal_correct_words", ['104', '104 90'])


