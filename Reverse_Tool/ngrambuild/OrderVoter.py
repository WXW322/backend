from ngrambuild.Base_voter import Base_voter
from Data_base.Data_redis.redis_deal import redis_convert
from common.readdata import *
from common.Converter.base_convert import word_converter
from Config.ve_strategy import ve_strategy

class OrderVoter(Base_voter):
    def __init__(self, fre_woc):
        super().__init__(fre_woc)
        self.voc['300'] = 1000000000

    def vote_for_item(self, item, start = 0):
        min_fre = 1000000000
        length = len(item)
        i = 1
        loc = -1
        while(i <= length):
            pre_itom = word_converter.convert_raw_to_text(item[0:i])
            if i < length:
                last_item = word_converter.convert_raw_to_text(item[i:length])
            else:
                last_item = '300'
            fre_sum = min(self.voc[pre_itom],self.voc[last_item])
            if fre_sum < min_fre:
                min_fre = fre_sum
                loc = i
            i = i + 1
        return loc



if __name__ == '__main__':
    prefix = ve_strategy().GetWordsKeys('OrderWords')
    normal_raw_words = redis_convert.read_from_redis('modbus_one_frequent_voter_abs_normal_0_0normal_correct_words')
    fre_vote = frequence_voter(normal_raw_words)
    datas = read_multity_dirs(["/home/wxw/data/modbusdata", "/home/wxw/data/modbus_github"])
    datas = get_puredatas(datas)
    first_data = datas[0]
    print(word_converter.convert_raw_to_text(first_data))
    print(fre_vote.vote_for_sequence(first_data,4))


