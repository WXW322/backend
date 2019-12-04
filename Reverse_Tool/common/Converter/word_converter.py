import sys
from .base_convert import Converter
from common.analyzer.analyzer_common import base_analyzer
from Data_base.Data_redis.redis_deal import redis_deal
from common.ranker import ranker
import time
import numpy as np
from Config.ve_strategy import ve_strategy
from common.Sorter.BaseSort import BaseSort

class word_convert(Converter):
    def __init__(self):
        super().__init__
        self.rank = ranker()
        self.bS = BaseSort()
        self.analysist = base_analyzer()

    def split_words(self, words, t_len):
        words_r = {}
        for i in range(1, t_len + 1):
            words_r[i] = []
        for word in words:
            words_r[len(word.split(' '))].append(word)
        return words_r

    def get_childs(self, word, words):
        w_len = len(word)
        t_children = []
        for l_word in words:
            if l_word[0:w_len] == word:
                t_children.append(l_word)
        return t_children

    def convert_word_order(self, words_s, words_l):
        start = 0
        w_orders = {}
        for word_s in words_s:
            w_childs = self.get_childs(word_s, words_l)
            w_orders[word_s] = start + int(len(w_childs)/2)
            start = start + int(len(w_childs))
        return w_orders

    def GetCorresOrder(self, WordChilds, WordVoc):
        WordDic = {}
        for Child in WordChilds:
            WordDic[Child] = WordVoc[Child]
        OrderWords = ranker().rank_dic(WordDic)
        TotalNum = sum([item[1] for item in OrderWords])
        Lo = 0
        TempSum = 0
        while(TempSum < TotalNum / 2):
            TempSum = TempSum + OrderWords[Lo][1]
            Lo = Lo + 1
        return Lo

    def ConvertWordToNumOrder(self, WordTarget, WordPrim, WordVoc):
        Start = 0
        WordOrders = {}
        for WordT in WordTarget:
            WordChilds = self.get_childs(WordT, WordPrim)
            WordOrders[WordT] = Start + self.GetCorresOrder(WordChilds, WordVoc)
            Start = Start + len(WordChilds)
        return WordOrders


    def ConvertDataToNgram(self, datas):
        pass

    def splitwords_bylen(self, raw_words, len_max):
        """
        :param words:
        :param raw_words:
        :param len_max:
        :return:
        """
        word_length = {}
        for i in range(1, len_max + 1):
            word_length[i] = []
        for word in raw_words:
            word_length[len(word.split(' '))].append((word, raw_words[word]))
        return word_length

    def itemtoborder(self, words):
        """
        :param words:tuple of words
        :return: the split border
        """
        words_rank = self.rank.rank_tulple(words)
        borders = [word[0] for word in words_rank]
        borders.append(words_rank[-1][1])
        return borders

    def ConvertwordToCntOrder(self, wA, wB):
        cntA = 0
        cntB = 0
        cntA = sum([w[1] for w in wA])
        cntB = sum([w[1] for w in wB])
        i = 0
        while(i < len(wA)):
            wA[i] = list(wA[i])
            wA[i][1] = (wA[i][1] * (cntB / cntA)) / 2
            i = i + 1
        return wA

    def ConvertRawWordsToOrder(self, rawwords, nrange, ordertype = "abs"):
        Analyzer = base_analyzer()
        WordRanker = ranker()
        Converter = word_convert()
        num_words = Converter.splitwords_bylen(rawwords, nrange)
        for len_word in num_words:
            num_words[len_word] = WordRanker.rank_words(num_words[len_word], reverse=True)
            #num_words[len_word] = WordRanker.rank_tulple(num_words[len_word], reverse=True)
        PrimeWords = [word[0] for word in num_words[nrange]]
        PrimeOrders = {}
        for i in range(len(PrimeWords)):
            PrimeOrders[PrimeWords[i]] = i
        OrderWords = {}
        OrderWords[nrange] = PrimeOrders
        start_time = time.time()
        for i in range(1, nrange):
            if ordertype == 'abs':
                OrderWords[i] = self.ConvertWordToNumOrder([word[0] for word in num_words[i]], PrimeWords, rawwords)
            elif ordertype == 'Set':
                OrderWords[i] = self.ConvertwordToCntOrder(num_words[i], num_words[nrange])
            else:
                OrderWords[i] = Converter.convert_word_order([word[0] for word in num_words[i]], PrimeWords)
        OrderWords = self.convert_order_to_raw(OrderWords)
        return OrderWords
        #DataWriter = redis_deal()
        #DataWriter.insert_to_redis('order_raw_words', OrderWords)



    def convert_order_to_raw(self, order_words):
        raw_words = {}
        print(order_words)
        for num_key in order_words:
            for w_key in order_words[num_key]:
                raw_words[w_key] = order_words[num_key][w_key]
        return raw_words

    def GetChildKey(self,t_dics,key):
        """
        function: get childs of words key
        t_dics:dict words table
        key: str key:words
        return: float entry of children
        """
        t_entrys = []
        for i in range(0,256):
            t_idom = key + ' ' + str(i)
            if t_idom in t_dics:
                t_entrys.append(t_dics[t_idom] / t_dics[key])
        t_fentry = 0
        t_fentry = self.analysist.get_enrty(t_entrys)
        return t_fentry

    def convert_raw_to_entry(self,t_dics,nrange):
        """
        function: get entry of ngrams
        t_dics: dict words vacabulary
        nrange: int length of words
        return:dict entry information of words
        """
        t_entrys = {}
        for key in t_dics:
            if(len(key.split(' ')) < nrange + 1):
                t_entrys[key] = self.GetChildKey(t_dics,key)
            else:
                t_entrys[key] = 0
        return t_entrys
        t_entrylist = {}
        for i in range(1,nrange + 1):
            t_entrylist[i] = []
        for key in t_entrys:
            t_entrylist[len(key.split(' '))].append(t_entrys[key])
        t_entrymean = {}
        t_entrystd = {}
        for i in range(1,nrange + 1):
            t_entrymean[i] = np.mean(np.array(t_entrylist[i]))
            t_entrystd[i] = np.std(np.array(t_entrylist[i]),ddof = 1)
        for key in t_entrys:
            if t_entrystd[len(key.split(' '))] == 0:
                t_entrys[key] = 0
            else:
                t_entrys[key] = (t_entrys[key] - t_entrymean[len(key.split(' '))]) / (t_entrystd[len(key.split(' '))])
        return t_entrys











if __name__ == '__main__':
    redis_read = redis_deal()
    word_converter = word_convert()
    prefix = ve_strategy().GetWordsKeys('OrderWords')
    OrderWords = redis_read.read_from_redis(prefix)
    OrderWords = word_converter.convert_order_to_raw(OrderWords)
    redis_read.insert_to_redis(prefix, OrderWords)
    print(word_converter.splitwords_bylen(OrderWords, 4)[1])
    #OrderWords = word_converter.convert_raw_word_to_order(RawWords)
    #OrderWords = word_converter.convert_order_to_raw(OrderWords)
    #OrderPrefix = ve_strategy().GetWordsKeys('OrderWords')
    #redis_read.insert_to_redis(OrderPrefix, OrderWords)
    #entry_words = word_converter.convert_raw_to_entry(raw_words, 5)
    #prefix = ve_strategy().get_strategy_str()
    #redis_read.insert_to_redis('{}_normal_entry_words'.format(prefix), entry_words)
    #order_words = redis_read.read_from_redis("order_raw_words")
    #raw_words = word_converter.convert_order_to_raw(order_words)
    #print(raw_words['0 6 255'], raw_words['1'])
    #word_converter.convert_raw_word_to_order(raw_words)






