from ngrambuild.pyngram import voters
from common.f_cg import transer
from common.readdata import *
from Data_base.Data_redis.redis_deal import redis_deal
from Config.ve_strategy import ve_strategy
from common.Converter.word_converter import word_convert
from common.Converter.base_convert import Converter
from ngrambuild.frequent_voter import frequence_voter
from ngrambuild.entry_voter import Entry_voter
from ngrambuild.OrderVoter import OrderVoter
from ngrambuild.Desiner import Desiner
from Config.UserConfig import UserConfig,VeConfig
import sys


class splitter:

    def __init__(self):
        self.prefix = ve_strategy().get_strategy_str()
        self.redis_read = redis_deal()
        self.parameters = ve_strategy().vote_parameters
        self.ngram = voters()

    def split_by_ve(self, messages, h, combine, model, v_way, T=0, r=0, ways="g"):
        voter = voters()
        split_messages = voter.single_message_voter(messages, h, combine, model, v_way, T, r)
        converter = transer()
        return converter.listtoids(split_messages)

    def split_by_order_ve(self, messages):
        voter = voters()
        redis_read = redis_deal()
        raw_words = redis_read.read_from_redis('order_raw_words')
        w_converter = word_convert()
        order_words = w_converter.convert_order_to_raw(raw_words)
        order_words['300'] = 1000000
        boundaries = voter.raw_boundary_generate(messages, order_words)
        return boundaries

    def split_by_entry(self, messages):
        keys = ve_strategy().GetWordsKeys("EntryWords")
        entry_words = None
        if self.redis_read.is_exist_key(keys):
            entry_words = self.redis_read.read_from_redis(keys)
        else:
            raw_keys = ve_strategy().GetWordsKeys("RawWords")
            raw_words = self.redis_read.read_from_redis(raw_keys)
            entry_words = word_convert().convert_raw_to_entry(raw_words, self.parameters['height'] + 1)
            self.redis_read.insert_to_redis(keys, entry_words)
        entry_voter = Entry_voter(entry_words)
        PrimBorders = entry_voter.vote_for_messages(messages, self.parameters['height'])
        FinalBorders = Desiner().VoteMultiM(PrimBorders, self.parameters['diff_measure'],
                                            self.parameters['decision_type'],
                                            self.parameters['Threshold_T'], self.parameters['Threshod_R'])
        return Converter().ConvertListToOrder(FinalBorders)


    def split_by_frequent(self, messages):
        prefix = ve_strategy().GetWordsKeys('FrequentWords')
        entry_words = None
        if self.redis_read.is_exist_key(prefix):
            frequent_words = self.redis_read.read_from_redis(prefix)
        else:
            raw_keys = ve_strategy().GetWordsKeys('RawWords')
            raw_words = self.redis_read.read_from_redis(raw_keys)
            frequent_words = Converter().ConvertRawToNormalFrequent(raw_words, self.parameters['height'] + 1)
            self.redis_read.insert_to_redis(prefix, frequent_words)
        frequent_voter = frequence_voter(frequent_words)
        PrimBorders = frequent_voter.vote_for_messages(messages, self.parameters['height'])
        FinalBorders = Desiner().VoteMultiM(PrimBorders, self.parameters['diff_measure'],
                                            self.parameters['decision_type'],
                                            self.parameters['Threshold_T'], self.parameters['Threshod_R'])
        return Converter().ConvertListToOrder(FinalBorders)

    def SplitByOrder(self, messages):
        key = ve_strategy().GetWordsKeys('OrderWords')
        if self.redis_read.is_exist_key(key):
            OrderWords = self.redis_read.read_from_redis(key)
        else:
            raw_keys = ve_strategy().GetWordsKeys('RawWords')
            raw_words = self.redis_read.read_from_redis(raw_keys)
            OrderWords = word_convert().ConvertRawWordsToOrder(raw_words, self.parameters['height'] + 1)
            self.redis_read.insert_to_redis(key, OrderWords)
        orderVoter = OrderVoter(OrderWords)
        PrimBorders = orderVoter.vote_for_messages(messages, self.parameters['height'])
        FinalBorders = Desiner().VoteMultiM(PrimBorders, self.parameters['diff_measure'],
                                            self.parameters['decision_type'],
                                            self.parameters['Threshold_T'], self.parameters['Threshod_R'])
        return Converter().ConvertListToOrder(FinalBorders)

    def VoterNameToBorders(self, VoterName, Messages):
        if VoterName == 'frequent':
            return self.split_by_frequent(Messages)
        elif VoterName == 'entry':
            return self.split_by_entry(Messages)
        else:
            return self.SplitByOrder(Messages)


    def CombineSplitBorders(self, messages, VoterA, VoterB):
        BorderA = self.VoterNameToBorders(VoterA, messages)
        BorderB = self.VoterNameToBorders(VoterB, messages)
        return Converter().MergeListGroup(BorderA, BorderB)


    def getFreVotes(self, ConfigParas, messages):
        Key = ConfigParas.getUserPathDynamic()
        freWords = self.ngram.getQueryFrequentWords(Key)
        freVoter = frequence_voter(freWords)
        primBorders = freVoter.vote_for_messages(messages, VeConfig.veParameters['height'])
        return primBorders

    def getEntryVotes(self, conFigParas, messages):
        key = conFigParas.getUserPathDynamic()
        entryWords = self.ngram.getQueryEntryWords(key)
        entryVoter = Entry_voter(entryWords)
        primBorders = entryVoter.vote_for_messages(messages, VeConfig.veParameters['height'])
        return primBorders








if __name__ == '__main__':
    raw_messages = read_multity_dirs(["/home/wxw/data/modbusdata", "/home/wxw/data/modbus_github"])
    pure_datas = get_puredatas(raw_messages)
    order_spliter = splitter()
    """
    get the words
    boundaries = order_spliter.split_by_order_ve(pure_datas)
    T_word_convert = word_convert()
    words_prim = T_word_convert.convert_words_byloc(boundaries)
    words_count = T_word_convert.get_words_count(words_prim)
    t_ranker = ranker()
    words_rank = t_ranker.rank_dic(words_count, True)
    print(words_rank)
    """








