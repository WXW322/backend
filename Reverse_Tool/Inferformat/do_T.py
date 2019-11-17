from Inferformat.treef_loc import treefL
import sys
from common.Model.canf import prime_b
from splitter.VE_spliter import splitter
from common.readdata import *
from Data_base.Data_redis.redis_deal import redis_deal
from Config.ve_strategy import ve_strategy
import json

def get_format_by_voting_expert(messages, h, combine, model, v_way, T, r):
    message_splitter = splitter()
    #message_split = message_splitter.split_by_ve(messages, h, combine, model, v_way, T, r)
    redis_dealer = redis_deal()
    strategy = ve_strategy().get_strategy_str()
    #redis_dealer.insert_to_redis('split' + strategy, json.dumps(message_split))
    message_split = redis_dealer.read_from_redis('split' + strategy)
    message_prim_format = {}
    for key in message_split:
        message_prim_format[key[0]] = prime_b(key[1])
    tree_builder = treefL(message_prim_format, int(0.1 * len(message_split)), 0.2)
    t_result = tree_builder.generate_T()
    t_result.depth_traverse()
    for f in t_result.result:
        print("format start")
        for node_i in f:
            print(node_i.loc)




def do_init():
    t_temp = []
    t_temp.append(prime_b([0,1,3,5,7]))
    t_temp.append(prime_b([0,1,3,5,9]))
    t_temp.append(prime_b([0,1,3,5,10]))
    t_temp.append(prime_b([0,2,4,6,7]))
    t_temp.append(prime_b([0,2,4,6,8]))
    t_temp.append(prime_b([0,2,4,6,10]))
    t_keys = {}
    for i, item in enumerate(t_temp):
        t_keys[i] = item
    tree_builder = treefL(t_keys, 3, 0.2)
    t_result = tree_builder.generate_T()
    t_result.depth_traverse()
    for f in t_result.result:
        print("format start")
        for node_i in f:
            print(node_i.loc)

def do_format_T(data_path, r_way, h, combine, model, v_way, T, r):
    datas = read_datas(data_path, r_way)
    datas = get_puredatas(datas)
    messages = add_tail(datas, h)
    get_format_by_voting_expert(messages, h, combine, model, v_way, T, r)

#do_format_T("/home/wxw/data/iec104", "single", 4, "yes", "abs", "normal", 0, 0)



