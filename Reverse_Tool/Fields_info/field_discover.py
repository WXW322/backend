from netzob.all import *
import sys
import time
from common.readdata import *
from common.ranker import ranker
from word_convert import word_convert
from splitter.VE_spliter import splitter
from log_info.logger import get_logger
from Config.Abtest import ABtest
from Config.const_config import log_path

class words_discover:
    def __init__(self):
        self.name = "words_deal"

    def infer_words_by_ve(self, data_path, r_way, h, combine, model, v_way, T, r):
        if type(data_path) == 'str':
            datas = read_datas(data_path, r_way)
        else:
            datas = read_multity_dirs(data_path, r_way)
        datas = get_puredatas(datas)
        ABtest_now = ABtest()
        datas = datas[0:int(len(datas) * ABtest_now.ratio)]
        #messages = add_tail(datas, h) # change
        messages = datas
        message_splitter = splitter()
        message_split = message_splitter.split_by_ve(messages, h, combine, model, v_way, T, r)
        t_now = time.strftime("%Y-%m-%d %H:%m:%s", time.localtime(time.time()))
        m_logger = get_logger(log_path + '/messge_splited_log' + t_now, 'msg_split')
        for message in message_split:
            m_logger.error(message)
        T_word_convert = word_convert()
        words_prim = T_word_convert.convert_words_byloc(message_split)
        p_logger = get_logger(log_path + '/p_log' + t_now, 'word_count')
        for key in words_prim:
            p_logger.error(key + str(words_prim[key].content))
        words_count = T_word_convert.get_words_count(words_prim)
        t_ranker = ranker()
        words_rank = t_ranker.rank_dic(words_count,True)
        return words_rank




