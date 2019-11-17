from Fields_info.field_discover import words_discover
from log_info.logger import get_logger, vote_pre
from Fields_info.fields_measure import Fields_measure
from Config.modbus import modbus
from common.f_cg import transer
from common.Converter.base_convert import Converter
import time
from Data_base.Data_redis.redis_deal import redis_deal
from common.readdata import read_datas, get_puredatas
from functools import cmp_to_key
from common.analyzer.analyzer_common import base_analyzer
from Config.log_config import log_path
from Config.ve_strategy import ve_strategy

ve_stra_str = ve_strategy().get_strategy_str()

analyzer = base_analyzer()

def cmp_word(word_one, word_two):
    start_one = int(word_one[0].split(' ')[0])
    start_two = int(word_two[0].split(' ')[0])
    if start_one < start_two:
        return 1
    elif start_one > start_two:
        return -1
    else:
        if word_one[1] >= word_two[1]:
            return 1
        else:
            return 0

def ve_word():
    word_dis = words_discover()
    word_redis = redis_deal()
    word_r = word_dis.infer_words_by_ve(["/home/wxw/data/modbusdata", "/home/wxw/data/modbus_github"], "single", 3, "yes", "abs", "loose", 0, 0)
    word_redis.insert_to_redis(ve_stra_str + 'word_rank_correct', word_r)
    word_pures = [word[0] for word in word_r]
    word_redis.insert_to_redis(ve_stra_str + 'word_pure_rank_correct', word_pures)
    word_transer = transer()
    modbus_w = modbus()
    word_t = word_transer.field_keys(modbus_w.fields)
    word_redis.insert_to_redis(ve_stra_str + 'word_true_correct', word_t)
    t_measure = Fields_measure(word_t, word_pures)
    t_cnt = t_measure.measure(1000)
    print(t_cnt)
    t_now = time.strftime("%Y-%m-%d %H:%m:%s", time.localtime(time.time()))
    words_logger = get_logger(log_path + '/word_log' + vote_pre + t_now, 'word_logger')
    words_logger.error(word_r)

def word_rank_result(key_true, key_test, rank_k, words_infer = None):
    word_redis = redis_deal()
    words_true = word_redis.read_from_redis(key_true)
    if words_infer == None:
        words_infer = word_redis.read_from_redis(key_test)
    i = 10
    t_measure = Fields_measure(words_true, words_infer)
    t_X = []
    t_Y = []
    while(i <= rank_k):
        t_ratio = t_measure.measure(i)
        t_X.append(i)
        t_Y.append(t_ratio)
        i = i + 10
    print(t_X)
    print(t_Y)

def raw_to_redis(file_path, r_way):
    datas = read_datas(file_path, r_way)
    datas = get_puredatas(datas)
    raw_datas = []
    converter =Converter()
    for data in datas:
        raw_datas.append(converter.convert_raw_to_text(data))
    key = file_path
    phrase_redis = redis_deal()
    phrase_redis.insert_to_redis(key, raw_datas)

def raw_to_log(file_path, r_way, protocol):
    datas = read_datas(file_path, r_way)
    datas = get_puredatas(datas)
    raw_datas = []
    converter =Converter()
    logger_raw = get_logger(log_path + '/' + protocol, 'raw_message_logger')
    i = 0
    for data in datas:
        logger_raw.error(str(i) + ':' + converter.convert_raw_to_text(data))


def show_raw_data(file_path):
    redis_dealer = redis_deal()
    datas = redis_dealer.read_from_redis(file_path)
    print(datas[0])

def show_data_frequent():
    redis_dealer = redis_deal()
    datas = redis_dealer.read_from_redis('/home/wxw/data/iec104/fre')
    i = 0
    print(type(datas))
    for key in datas:
        print(key)


def get_new_correct_rank_words(key):
    word_redis = redis_deal()
    correct_words = word_redis.read_from_redis(key)
    correct_words = analyzer.filter_words(correct_words, 60)
    correct_words.sort(key=cmp_to_key(cmp_word), reverse = True)
    pure_correct_words = [word[0] for word in correct_words]
    word_rank_result('aa', 'bb', 100, pure_correct_words)



#show_raw_data("/home/wxw/data/iec104")
#word_rank_result('word_true', 'word_pure', 500)
#raw_to_redis("/home/wxw/data/iec104", 'single')
#raw_to_log("/home/wxw/data/modbusdata", 'single', 'modbus')
#show_raw_data("/home/wxw/data/iec104")
#show_data_frequent()
#ve_word()
#get_new_correct_rank_words('word_rank_correct')
