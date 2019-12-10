from netzob.all import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np
import time
from log_info.logger import get_logger, vote_pre
from common.readdata import *
from Config.ve_strategy import ve_strategy
from Config.log_config import log_path
from Config.encode_types import Message_encoder
from common.Converter.base_convert import Converter
from Data_base.Data_redis.redis_deal import redis_deal
from Config.UserConfig import UserConfig
from Config.VeConfig import VeConfig
from common.Converter.word_converter import word_convert
import sys

now_time = time.strftime("%Y-%m-%d %H:%m:%s", time.localtime(time.time()))
voter_logger = get_logger(log_path + '/message_vote' + vote_pre + now_time, 'messagedetaillogger')
ve_parameter = ve_strategy().vote_parameters
redis_writer = redis_deal()
redis_prefix = ve_strategy().get_strategy_str()
 
class voters:
    def __init__(self):
        self.words_fre = None
        self.words_table = None
        self.words_entry = None
        self.glvotes = None
        self.svotes = None
        self.redisDeal = redis_deal()
        self.wCvert = word_convert()

    def query_key(self,key):
        return self.words_table[key],self.words_fre[key],self.words_entry[key]

    def query_keys(self,keys):
        f_r = {}
        for key in keys:
            f_r[key] = self.query_key(key)
        return f_r

    def get_single_message_with_h(self, message):
        """
                converse a message to n-gram item
                message: a list o bytes
                return : str of n-gram items
                """
        t_len = len(message)
        i = 0
        t_flist = ''
        h = ve_parameter['height']
        while (i < t_len):
            if (len(t_flist) == 0):
                if Message_encoder.encode_type == 'location_based':
                    t_flist = t_flist + str(i) + '_' + str(message[i])
                else:
                    t_flist = t_flist + str(message[i])
            else:
                if Message_encoder.encode_type == 'location_based':
                    t_flist = t_flist + ' ' + str(i) + '_' + str(message[i])
                else:
                    t_flist = t_flist + ' ' + str(message[i])
            i = i + 1
        i = 0
        while(i < h):
            t_flist = t_flist + ' ' + ve_parameter['stop_words']
            i = i + 1
        return t_flist


    def get_single_messages(self,message):
        """
        converse a message to n-gram item
        message: a list o bytes
        return : str of n-gram items
        """
        t_list = []
        t_len = len(message)
        i = 0
        t_flist = ''
        while(i < t_len):
           if(len(t_flist) == 0):
               if Message_encoder.encode_type == 'location_based':
                   t_flist = t_flist + str(i) + '_' + str(message[i])
               else:
                   t_flist = t_flist + str(message[i])
           else:
               if Message_encoder.encode_type == 'location_based':
                   t_flist = t_flist + ' ' + str(i) + '_' + str(message[i])
               else:
                   t_flist = t_flist + ' ' + str(message[i])
           i = i + 1
        return t_flist

    def printm(self,message):
        t_len = len(message)
        i = 0
        while(i < t_len):
            print(message[i])
            i = i + 1

    def get_messages(self,messages):
        """
        function: converse messages to n-gram items
        messages: a list of message
        t_lists: str sentence lists
        """
        t_lists = ''
        for message in messages:
            if(len(t_lists) == 0):
                t_lists = t_lists + self.get_single_message_with_h(message)
            else:
                t_lists = t_lists + '. ' + self.get_single_message_with_h(message)
        return t_lists

    def get_splitsmessages(self,messages):
        t_lists = []
        for message in messages:
            t_lists.append(self.get_single_messages(message))
        return t_lists

    def get_keywords(self,messages,valuen):
        """
        function : get frequent of each words
        messages: str multiple sentences
        t_dics: dict words and its frequent
        """
        t_inputs = [self.get_messages(messages)]
        vetorizer = CountVectorizer(ngram_range=(1,valuen),stop_words=[' ','.'],token_pattern='(?u)\\b\\w\\w*\\b')
        X = vetorizer.fit_transform(t_inputs)
        t_arrays = np.squeeze(X.toarray())
        words = vetorizer.get_feature_names()
        t_len = len(words)
        t_dics = {}
        i = 0
        while(i < t_len):
            t_dics[words[i]] = int(str(t_arrays[i]))
            i = i + 1
        self.words_table = t_dics
        #redis_writer.insert_to_redis('raw_words', t_dics)
        return self.filter_words(t_dics)

    def filter_words(self, t_dic):
        stop_word = ve_parameter['stop_words']
        t_words_new = {}
        for key in t_dic:
            if key.find(stop_word) == -1:
                t_words_new[key] = t_dic[key]
        return t_words_new



    def get_frequent(self,t_dics,nrange):
        """
        function: caculate normalized frequence of words
        t_dics: dict words and its frequent
        nrange:the length of words
        t_frer: dict words and its frequence
        """
        t_fredic = {}
        t_biaozhun = {}
        t_mean = {}
        t_std = {}
        for i in range(1,nrange + 1):
            t_fredic[i] = []
            t_biaozhun[i] = []
        for key in t_dics:
            t_fredic[len(key.split(' '))].append(t_dics[key])

        for i in range(1,nrange + 1):
            t_fredic[i] = sum(t_fredic[i])
        t_frer = {}
        for key in t_dics:
            t_frer[key] = -np.log(t_dics[key] / t_fredic[len(key.split(' '))])
            t_biaozhun[len(key.split(' '))].append(t_frer[key])
        #for key in t_biaozhun:
         #   print(key)
          #  print(t_biaozhun[key])
        #redis_writer.insert_to_redis('raw_frequent', t_frer)
        for i in range(1,nrange + 1):
            t_mean[i] = np.mean(np.array(t_biaozhun[i]))
            t_std[i] = np.std(np.array(t_biaozhun[i]),ddof = 1)
        for key in t_dics:
            if t_std[len(key.split(' '))] != 0:
                t_frer[key] = (t_frer[key] - t_mean[len(key.split(' '))]) / t_std[len(key.split(' '))]
            else:
                t_frer[key] = 0
        self.words_fre = t_frer
        return t_frer

    def get_childs(self,t_dics,key):
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
                t_entrys.append(t_dics[t_idom])
        t_fentry = 0
        for entry in t_entrys:
            t_fentry = t_fentry + (entry / t_dics[key]) * np.log(entry / t_dics[key])
        return -t_fentry 
        

    def get_backentry(self,t_dics,nrange):
        """
        function: get entry of ngrams
        t_dics: dict words vacabulary
        nrange: int length of words
        return:dict entry information of words
        """
        t_entrys = {}
        for key in t_dics:
            if(len(key.split(' ')) < nrange + 1):
                t_entrys[key] = self.get_childs(t_dics,key)
            else:
                t_entrys[key] = 0
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

    def getOrder(self, rawwords, nrange):
        orderWords = self.wCvert.ConvertRawWordsToOrder(rawwords, nrange)
        return orderWords


    def getQueryWords(self, key, msgs=None, wType='G'):
        key = key + '_' + 'RawWords'
        keyWords = {}
        if self.redisDeal.is_exist_key(key) and wType == 'B':
            keyWords = self.redisDeal.read_from_redis(key)
        else:
            messages = msgs
            #messages = read_datas(UserConfig.path, 'single')
            #messages = get_puredatas(messages)
            keyWords = self.get_keywords(messages, VeConfig.veParameters['height']+1)
            self.redisDeal.insert_to_redis(key, keyWords)
        return keyWords

    def getQueryFrequentWords(self, key, msgs = None, wType='M'):
        freWords = {}
        freKey = key + '_' + 'FreWords'
        if self.redisDeal.is_exist_key(freKey) and wType == 'G':
            freWords = self.redisDeal.read_from_redis(freKey)
        else:
            rawWords = self.getQueryWords(key, msgs)
            freWords = self.get_frequent(rawWords, VeConfig.veParameters['height'] + 1)
            self.redisDeal.insert_to_redis(freKey, freWords)
        return freWords

    def getQueryEntryWords(self, key, msgs, wType='M'):
        entryWords = {}
        entryKey = key + '_' + 'EntryWords'
        if self.redisDeal.is_exist_key(entryKey) and wType=='G':
            entryWords = self.redisDeal.read_from_redis(entryKey)
        else:
            rawWords = self.getQueryWords(key, msgs)
            entryWords = self.get_backentry(rawWords, VeConfig.veParameters['height'] + 1)
            self.redisDeal.insert_to_redis(entryKey, entryWords)
        return entryWords

    def getQueryMsgWords(self, messages, key=' '):
        keyR = key + '_' + 'RawWords'
        keyWords = {}
        if self.redisDeal.is_exist_key(keyR):
            keyWords = self.redisDeal.read_from_redis(keyR)
        else:
            keyWords = self.get_keywords(messages, VeConfig.veParameters['height']+1)
            if key != ' ':
                self.redisDeal.insert_to_redis(key, keyWords)
        return keyWords

    def getQueryMsgFrequentWords(self, messages, key=' '):
        freWords = {}
        freKey = key + '_' + 'FreWords'
        if self.redisDeal.is_exist_key(freKey):
            freWords = self.redisDeal.read_from_redis(freKey)
        else:
            rawWords = self.getQueryMsgWords(messages, key)
            freWords = self.get_frequent(rawWords, VeConfig.veParameters['height'] + 1)
            if key != ' ':
                self.redisDeal.insert_to_redis(freKey, freWords)
        return freWords

    def getQueryMsgEntryWords(self, messages, key=' '):
        entryWords = {}
        entryKey = key + '_' + 'EntryWords'
        if self.redisDeal.is_exist_key(entryKey):
            entryWords = self.redisDeal.read_from_redis(entryKey)
        else:
            rawWords = self.getQueryMsgWords(messages, key)
            entryWords = self.get_backentry(rawWords, VeConfig.veParameters['height'] + 1)
            if key != ' ':
                self.redisDeal.insert_to_redis(entryKey, entryWords)
        return entryWords

    def getQueryMsgOrderWords(self, messages, key=' '):
        orderWords = {}
        orderKey = key + '_' + 'OrderWords'
        if self.redisDeal.is_exist_key(orderKey):
            orderWords = self.redisDeal.read_from_redis(orderKey)
        else:
            rawWords = self.getQueryMsgWords(messages, key)
            orderWords = self.getOrder(rawWords, VeConfig.veParameters['height'] + 1)
            if key != ' ':
                self.redisDeal.insert_to_redis(orderKey, orderWords)
        return orderWords

    def getOrderWords(self, key):
        entryWords = {}
        entryKey = key + '_' + 'OrderWords'
        if self.redisDeal.is_exist_key(entryKey):
            entryWords = self.redisDeal.read_from_redis(entryKey)
        else:
            rawWords = self.getQueryWords(key)
            #orderWords = self.getOrder(ra)
            #entryWords = self.(rawWords, VeConfig.veParameters['height'] + 1)
            self.redisDeal.insert_to_redis(entryKey, entryWords)
        return entryWords

    def s2key(self, ses, start=None):
        """
        function:converse a data sequence to words
        ses: bytes sequences
        return: str words
        """
        s_f = ""
        for s in ses:
            if start == None:
                if len(s_f) == 0:
                    s_f = s_f + str(s)
                else:
                    s_f = s_f + ' ' + str(s)
            else:
                if len(s_f) == 0:
                    s_f = str(start) + '_' + str(s)
                else:
                    s_f = s_f + ' ' + str(start) + '_' + str(s)
                start = start + 1
        return s_f

    def vote_item(self,itom_s,t_frer,t_entrys, start=0):
        """
        function: get vote location of single item
        itom_s: bytes sequence
        t_frer: dict frequent table
        t_entrys:dict entry table

        """
        t_len = len(itom_s)
        i = 1
        t_min_fre = 100
        t_max_entry = -100
        t_fre_lo = -1
        t_entry_lo = -1
        while(i <= t_len):
            t_pre = self.s2key(itom_s[0:i])
            if i < t_len:
                t_last = self.s2key(itom_s[i:t_len])
            else:
                t_last = "300"
            t_fre = t_frer[t_pre] + t_frer[t_last]
            t_entry = t_entrys[t_pre]
            if t_fre < t_min_fre:
                t_min_fre = t_fre
                t_fre_lo = i
            if t_entry > t_max_entry:
                t_max_entry = t_entry
                t_entry_lo = i
            i = i + 1
        return t_fre_lo,t_entry_lo

    def order_item_vote(self, itom_s, order_words):
        """
        vote words by orders
        :param itom_s:
        :param order_words:
        :return:
        """
        t_lo = 0
        t_len = len(itom_s)
        i = 1
        t_min_order = 10000000
        t_order_lo = -1
        while (i <= t_len):
            t_pre = self.s2key(itom_s[0:i])
            if i < t_len:
                t_last = self.s2key(itom_s[i:t_len])
            else:
                t_last = "300"
            t_pre_order = order_words[t_pre]
            t_last_order = order_words[t_last]
            t_order_w = min(t_pre_order, t_last_order)
            if t_order_w < t_min_order:
                t_min_order = t_order_w
                t_order_lo = i
            i = i + 1
        return t_order_lo

    def vote_sequence(self,sequence,win_L,t_frer,t_entrys):
        """
        get voting result of a sequence
        sequnce:a message
        t_frer:frequent dict
        t_entrys:entry dict
        t_los: a location list
        win_L:size of ngram
        """
        t_len = len(sequence)
        i = 0
        f_fres = {}
        f_entrys = {}
        while(i < t_len):
            if i < t_len - win_L:
                t_fre,t_entry = self.vote_item(sequence[i:i+win_L],t_frer,t_entrys, i)
            else:
                t_fre,t_entry = self.vote_item(sequence[i:t_len],t_frer,t_entrys, i)
            t_f_item = i + t_fre
            t_e_item = i + t_entry
            if t_f_item not in f_fres:
                f_fres[t_f_item] = 1
            else:
                f_fres[t_f_item] = f_fres[t_f_item] + 1
            if t_e_item not in f_entrys:
                f_entrys[t_e_item] = 1
            else:
                f_entrys[t_e_item] = f_entrys[t_e_item] + 1
            i = i + 1
        i = 0
        while(i < win_L):
            if i in f_fres:
                f_fres[i] = f_fres[i] * (win_L / i)
            if i in f_entrys:
                f_entrys[i] = f_entrys[i] * (win_L / i)
            i = i + 1
        return f_fres,f_entrys

    def order_vote_sequence(self, sequence, win_L, order_words):
        """
        :param sequence:
        :param win_L:
        :param order_words:
        :return:
        """
        t_len = len(sequence)
        i = 0
        f_orders = {}
        while (i < t_len):
            if i < t_len - win_L:
                t_order = self.order_item_vote(sequence[i:i + win_L], order_words)
            else:
                t_order = self.order_item_vote(sequence[i:t_len], order_words)
            order_item = i + t_order
            if order_item not in f_orders:
                f_orders[order_item] = 1
            else:
                f_orders[order_item] = f_orders[order_item] + 1
            i = i + 1
        i = 0
        while (i < win_L):
            if i in f_orders:
                f_orders[i] = f_orders[i] * (win_L / i)
            i = i + 1
        return f_orders



    def vote_for_single_message(self,t_los, diff_measure, way,T = 0,r = 0):
        """
        funtion: get final los for one messages
        t_los:vote locations(dict)
        way:vote strategy:str
        T:vote threshold:int
        return: final locations(set)
        """
        t_flos = []
        for key in t_los:
            t_now = t_los[key]
            pre_key = key - 1
            last_key = key + 1
            t_pre = 0 if pre_key not in t_los else t_los[pre_key]
            t_last = 0 if last_key not in t_los else t_los[last_key]
            if diff_measure == "abs" and way == "normal":
                if t_now > T and t_now > t_pre and t_now > t_last:
                    t_flos.append(key)
            elif diff_measure == "abs" and way == "loose":
                if key != 1:
                    if t_now > T and ((t_now > t_pre) or (t_now > t_last)):
                        t_flos.append(key)
                else:
                    if t_now > T and ((t_now > t_pre) and (t_now > t_last)):
                        t_flos.append(key)
            elif diff_measure == "re" and way == "normal":
                if key != 1:
                    if t_now > T and (((t_pre == 0) or (t_now/t_pre > 1 + r)) and ((t_last == 0) or (t_now/t_last > 1 + r))):
                        t_flos.append(key)
                else:
                    if t_now > T and ((t_last == 0) or (t_now/t_last > 1 + r)):
                        t_flos.append(key)
            elif diff_measure == "re" and way == "loose":
                if key != 1:
                    if t_now > T and (((t_pre == 0) or (t_now/t_pre > 1 + r)) or ((t_last == 0) or (t_now/t_last > 1 + r))):
                        t_flos.append(key)
                else:
                    if t_now > T and ((t_last == 0) or (t_now/t_last > 1 + r)):
                        t_flos.append(key)
            else:
                print("error")
        return t_flos




    def vote_for_single_message_improve(self, t_los):
        """
        funtion: get final los for one messages
        t_los:vote locations(dict)
        way:vote strategy:str
        T:vote threshold:int
        return: final locations(set)
        """
        diff_measure = ve_parameter['diff_measure']
        decision_type = ve_parameter['decision_type']
        threshold_T = ve_parameter['threshold_T']
        threshold_R = ve_parameter['threshold_R']
        threshold_max = ve_parameter['threshold_max']
        t_flos = []
        for key in t_los:
            t_now = t_los[key]
            pre_key = key - 1
            last_key = key + 1
            t_pre = 0 if pre_key not in t_los else t_los[pre_key]
            t_last = 0 if last_key not in t_los else t_los[last_key]
            if diff_measure == "abs" and decision_type == "normal":
                if t_now > threshold_max or (t_now > threshold_T and t_now > t_pre and t_now > t_last):
                    t_flos.append(key)
            elif diff_measure == "abs" and decision_type == "loose":
                if key != 1:
                    if t_now > threshold_max or (t_now > threshold_T and ((t_now > t_pre) or (t_now > t_last))):
                        t_flos.append(key)
                else:
                    if t_now > threshold_max or (t_now > threshold_T and ((t_now > t_pre) and (t_now > t_last))):
                        t_flos.append(key)
            elif diff_measure == "re" and decision_type == "normal":
                if key != 1:
                    if t_now > threshold_max or (t_now > threshold_T and (((t_pre == 0) or (t_now/t_pre > 1 + threshold_R)) and ((t_last == 0) or (t_now/t_last > 1 + threshold_R)))):
                        t_flos.append(key)
                else:
                    if t_now > threshold_max or (t_now > threshold_T and ((t_last == 0) or (t_now/t_last > 1 + threshold_R))):
                        t_flos.append(key)
            elif diff_measure == "re" and decision_type == "loose":
                if key != 1:
                    if t_now > threshold_max or (t_now > threshold_T and (((t_pre == 0) or (t_now/t_pre > 1 + threshold_R)) or ((t_last == 0) or (t_now/t_last > 1 + threshold_R)))):
                        t_flos.append(key)
                else:
                    if t_now > threshold_max or (t_now > threshold_T and ((t_last == 0) or (t_now/t_last > 1 + threshold_R))):
                        t_flos.append(key)
            else:
                print("error")
        return t_flos

    def tulple2dic(self,tulple):
        t_dic = {}
        for item in tulple:
            t_dic[item[0]] = item[1]
        return t_dic

     
    def get_voter(self,sequences,way,T):
        """
        function: get result for a sequece
        sequence:list of messages:list
        way:vote stratagy:string
        T:threshold int
        return:a list of final locations
        """
        t_fsequence = []
        for t_setemp in sequences:
            t_temp_lo = sorted(t_setemp.items(),key = lambda x:x[0])
            print(t_temp_lo)
            t_temp_lo = self.tulple2dic(t_temp_lo)
            t_fsequence.append(self.vote_for_single_message(t_temp_lo,way,T))
        return t_fsequence

    def get_single_votes(self, sentence):
        t_lonum = {}
        for key in sentence:
            if key not in t_lonum:
                t_lonum[key] = 1
            else:
                t_lonum[key] = t_lonum[key] + 1
        return t_lonum

    def get_gvotes(self,sentences):
        """
        F: get global voting results
        sentences: list of bytes (messages set)
        way:caculate ways
        """
        t_flos = {}
        for sentence in sentences:
            for key in sentence:
                if key not in t_flos:
                    t_flos[key] = sentence[key]
                else:
                    t_flos[key] = t_flos[key] + sentence[key]
        return t_flos

    def merge_splits(self,seq1,seq2):
        s_los = set()
        for key in seq1:
            s_los.add(key)
        for key in seq2:
            s_los.add(key)
        l_los = list(s_los)
        l_los.sort()
        return l_los
 
    def filter_los(self,los,length):
        t_los = 0
        drop_keys = []
        for key in los:
            if key > length:
                drop_keys.append(key)
            if key == length:
                t_los = 1
        for key in drop_keys:
            los.pop(key)
        if t_los == 0:
            los[length] = 1
        return los

    def single_message_voter(self, messages, h, voters = "both", diff_measure = "abs", v_way = "normal", T=0, r=0):
        h = ve_parameter['height']
        voters = ve_parameter['voters']
        diff_measure = ve_parameter['diff_measure']
        v_way = ve_parameter['decision_type']
        T = ve_parameter['Threshold_T']
        r = ve_parameter['Threshod_R']
        redis_raw_word_keys = redis_prefix + 'correct_raw_words'
        if redis_writer.is_exist_key(redis_raw_word_keys):
            t_dics = redis_writer.read_from_redis(redis_raw_word_keys)
        else:
            t_dics = self.get_keywords(messages,h + 1)
            redis_writer.insert_to_redis(redis_prefix + 'correct_raw_words', t_dics)
        redis_normal_word_key = redis_prefix + 'normal_correct_words'
        if redis_writer.is_exist_key(redis_normal_word_key):
            t_fres = redis_writer.read_from_redis(redis_normal_word_key)
        else:
            t_fres = self.get_frequent(t_dics,h + 1)
            t_fres["300"] = 0
            redis_writer.insert_to_redis(redis_prefix + 'normal_correct_words', t_fres)
        self.words_fre = t_fres
        t_entrys = self.get_backentry(t_dics,h + 1)
        self.words_entry = t_entrys
        self.words_table = t_dics
        f_boundaries = []
        voters = ve_parameter['voters']
        raw_conv = Converter()
        for i in range(len(messages)):
            t_fre_r,t_entry_r = self.vote_sequence(messages[i],h,t_fres,t_entrys)
            #t_fre_r = self.filter_los(t_fre_r, int(len(messages[i]) - h)) # change
            #t_entry_r = self.filter_los(t_entry_r, int(len(messages[i]) - h)) # change
            if(voters == 'both'):
                t_fre_votes = self.get_gvotes([t_fre_r, t_entry_r])
                #voter_logger.error('raw: ' + str(t_fre_votes))
                t_candidate_loc = self.vote_for_single_message(t_fre_votes, diff_measure, v_way, T, r)
                #voter_logger.error("voted: " + str(i) + " " + str(t_candidate_loc))
                f_boundaries.append(t_candidate_loc)
            elif voters == 'frequent_voter':
                voter_logger.error('raw: ' + str(raw_conv.convert_raw_to_text(messages[i])))
                voter_logger.error('raw + frequent: ' + str(t_fre_r))
                t_candidate_loc = self.vote_for_single_message(t_fre_r, diff_measure, v_way, T, r)
                voter_logger.error("voted: " + str(i) + " " + str(t_candidate_loc))
                f_boundaries.append(t_candidate_loc)
            else:
                #voter_logger.error('raw + entry: ' + str(t_fre_r))
                t_candidate_loc = self.vote_for_single_message(t_entry_r, diff_measure, v_way, T, r)
                #voter_logger.error("voted: " + str(i) + " " + str(t_candidate_loc))
                f_boundaries.append(t_candidate_loc)
        return f_boundaries

    def raw_boundary_generate(self, messages, order_wors):
        """
        :param messages:
        :param order_wors:
        :return:
        """
        h = ve_parameter['height']
        raw_orders = []
        for message in messages:
            raw_orders.append(self.order_vote_sequence(message, h, order_wors))
        return raw_orders

    def messages_boundary_generate(self, prim_orders, order_words):
        """
        :param messages:
        :param order_words:
        :return:
        """
        h = ve_parameter['height']
        voters = ve_parameter['voters']
        diff_measure = ve_parameter['diff_measure']
        v_way = ve_parameter['decision_type']
        T = ve_parameter['Threshold_T']
        r = ve_parameter['Threshod_R']
        f_boundaries = []
        for prim_order in prim_orders:
            f_boundaries.append(self.vote_for_single_message(prim_order, diff_measure, v_way, T, r))
        return f_boundaries


    def single_message_voter_improve(self, messages):
        height = ve_parameter['height']
        voters = ve_parameter['voters']
        diff_measure = ve_parameter['diff_measure']
        decision_type = ve_parameter['decision_type']
        threshold_T = ve_parameter['threshold_T']
        threshold_R = ve_parameter['threshold_R']
        threshold_max = ve_parameter['threshold_max']
        t_dics = self.get_keywords(messages, height + 1)
        t_fres = self.get_frequent(t_dics, height + 1)
        t_fres["300"] = 0
        self.words_fre = t_fres
        t_entrys = self.get_backentry(t_dics, height + 1)
        self.words_entry = t_entrys
        self.words_table = t_dics
        f_boundaries = []
        for i in range(len(messages)):
            t_fre_r, t_entry_r = self.vote_sequence(messages[i], height, t_fres, t_entrys)
            t_fre_r = self.filter_los(t_fre_r, int(len(messages[i]) - height))
            t_entry_r = self.filter_los(t_entry_r, int(len(messages[i]) - height))
            if (voters == 'both'):
                t_fre_votes = self.get_gvotes([t_fre_r, t_entry_r])
                #voter_logger.error('raw: ' + str(t_fre_votes))
                t_candidate_loc = self.vote_for_single_message_improve(t_fre_votes, voters, diff_measure, T, r)
                #voter_logger.error("voted: " + str(i) + " " + str(t_candidate_loc))
                f_boundaries.append(t_candidate_loc)
            elif voters == 'frequent_voter':
                #voter_logger.error('raw + frequent: ' + str(t_fre_r))
                t_candidate_loc = self.vote_for_single_message_improve(t_fre_r, model, v_way, T, r)
                #voter_logger.error("voted: " + str(i) + " " + str(t_candidate_loc))
                f_boundaries.append(t_candidate_loc)
            else:
                #voter_logger.error('raw + entry: ' + str(t_fre_r))
                t_candidate_loc = self.vote_for_single_message_improve(t_entry_r, model, v_way, T, r)
                #voter_logger.error("voted: " + str(i) + " " + str(t_candidate_loc))
                f_boundaries.append(t_candidate_loc)
        return f_boundaries




    def get_info(self,messages,h,ways="g",combine="no",model="abs",v_way="normal",T=0,r=0,stren = "no"):
        t_dics = self.get_keywords(messages,h + 1)
        t_fres = self.get_frequent(t_dics,h + 1)
        t_fres["300"] = 0
        self.words_fre = t_fres
        t_entrys = self.get_backentry(t_dics,h + 1)
        self.words_entry = t_entrys
        self.words_table = t_dics
        t_mes_frelos = []
        t_me_entry_los = []
        for i in range(len(messages)):
            t_fre_r,t_entry_r = self.vote_sequence(messages[i],h,t_fres,t_entrys)
            t_fre_r = self.filter_los(t_fre_r,int(len(messages[i]) - h))
            t_entry_r = self.filter_los(t_entry_r,int(len(messages[i]) - h))
            t_mes_frelos.append(t_fre_r)
            t_me_entry_los.append(t_entry_r)
        if ways == "g" and combine == "no":
            lo_f = self.get_gvotes(t_mes_frelos)
            lo_e = self.get_gvotes(t_me_entry_los)
            t_lastone = lo_f[max(lo_f,key = lo_f.get)]
            t_lasttwo = lo_e[max(lo_e,key = lo_e.get)]
            last_f = max(t_lastone,t_lasttwo)
            lo_vf = self.vote_for_single_message(lo_f, model, v_way, T, r)
            lo_ve = self.vote_for_single_message(lo_e, model, v_way, T, r)
            t_results = self.merge_splits(lo_vf,lo_ve)
            if t_results[-1] < last_f:
                t_results.append(-1)
            print(t_results)

        elif ways == "g" and combine == "yes":
            sum_los = []
            sum_los.extend(t_mes_frelos)
            sum_los.extend(t_me_entry_los)
            sum_Tlos = self.get_gvotes(sum_los)
            t_lasts = sum_Tlos[-1]
            t_results = self.vote_for_single_message(sum_Tlos,way=v_way)
            if(t_results[-1] < t_lasts):
                t_results.append(-1)
        
        return t_results


        
                

if __name__ == '__main__':
    voter = voters()
    single_message = voter.get_keywords([[10, 10, 11, 12, 15], [10, 10, 11]], 4)
    print(voter.filter_words(single_message))



"""        
        
datas = readdata.read_datas('/home/wxw/data/iec104/')
messages = readdata.get_puredatas(datas)
            
start = time.time()
voter = voters()
t_r = voter.get_info(messages,4,r=0.1)
print(t_r)
print(len(voter.words_table))
"""
"""
t_dics = voter.get_keywords(messages,5)
t_fres = voter.get_frequent(t_dics,6)
t_fres["300"] = 0
t_entrys = voter.get_backentry(t_dics,6)
t_mes_frelos = []
t_me_entry_los = []
for i in range(5):
    t_fre_r,t_entry_r = voter.vote_sequence(messages[i],5,t_fres,t_entrys)
    t_me_entry_los.append(t_entry_r)
#t_results = voter.get_voter(t_mes_frelos,'normal',0)
t_results = voter.get_voter(t_me_entry_los,'normal',0)    
print(t_results)
end = time.time()
print(end - start)
"""
           
