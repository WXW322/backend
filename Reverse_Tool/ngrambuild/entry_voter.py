from ngrambuild.Base_voter import Base_voter
from Data_base.Data_redis.redis_deal import redis_convert
from common.readdata import *
from common.Converter.base_convert import word_converter
import sys

class Entry_voter(Base_voter):
    def __init__(self, fre_woc):
        super().__init__(fre_woc)
        self.voc['300'] = 0

    def vote_for_item(self, item, start = 0):
        max_entry = -100
        length = len(item)
        i = 1
        loc = -1
        while(i <= length):
            now_itom = word_converter.convert_raw_to_text(item[0:i])
            entry_num = self.voc[now_itom]
            if entry_num > max_entry:
                max_entry = entry_num
                loc = i
            i = i + 1
        return loc

