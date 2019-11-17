import json
import sys
import redis
from Config.ve_strategy import ve_strategy

class redis_deal:
    def __init__(self, host = 'localhost', port = '6379'):
        self.port = port
        self.host = host
        self.link = redis.StrictRedis(host=self.host, port=self.port, decode_responses=True)

    def insert_to_redis(self, key, datas):
        if self.link.exists(key):
            self.link.delete(key)
        self.link.set(key, json.dumps(datas))

    def read_from_redis(self, key):
        if not self.link.exists(key):
            return None
        else:
            return json.loads(self.link.get(key))

    def is_exist_key(self, key):
        if self.link.exists(key):
            return True
        else:
            return False

redis_convert = redis_deal()

if __name__ == '__main__':
    redis_dealer = redis_deal()
    prefix = ve_strategy().GetWordsKeys("OrderWords")
    Iec104 = redis_dealer.read_from_redis(prefix)
    print(Iec104)
    #NewPrefix = ve_strategy().GetWordsKeys('RawWords')
    #redis_dealer.insert_to_redis(NewPrefix, ModbusData)
    #FrequentWordsPrim = redis_dealer.read_from_redis('modbus_one_frequent_voter_abs_normal_0_0_normal_entry_words')
    #rawWordsSecond = redis_dealer.read_from_redis(prefix);
    #redis_dealer.insert_to_redis(prefix, FrequentWordsPrim)
    #rawWordsSecond = redis_dealer.read_from_redis(prefix);
    #print(MeasureAb().Measure(FrequentWordsPrim, rawWordsSecond))

    #raw_words_ones = redis_dealer.read_from_redis(raw_words_key)

    #redis_dealer.insert_to_redis(raw_words_key, raw_words_values)






