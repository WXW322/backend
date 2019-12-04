from ..readdata import *
import numpy as np
from Config.ve_strategy import ve_strategy
from sklearn.feature_extraction.text import CountVectorizer
from Data_base.Data_redis.redis_deal import redis_convert
from Config.VeConfig import VeConfig

class Converter:
    def __init__(self):
        pass

    def convert_raw_to_text(self, message):
        phrase = ''
        for i in range(len(message)):
            if(len(phrase) == 0):
                phrase = phrase + str(message[i])
            else:
                phrase = phrase + ' ' + str(message[i])
        return phrase

    def ConvertRawToLengthText(self, message, delimeter=' '):
        """
        converse a message to n-gram item
        message: a list o bytes
        return : str of n-gram items
        """
        t_list = []
        t_len = len(message)
        i = 0
        t_flist = ''
        h = VeConfig.veParameters['height']
        while (i < t_len):
            if (len(t_flist) == 0):
                t_flist = t_flist + str(message[i])
            else:
                t_flist = t_flist + delimeter + str(message[i])
            i = i + 1
        i = 0
        while(i < h):
            #t_flist = t_flist + delimeter + ve_strategy().vote_parameters['stop_words']
            t_flist = t_flist + delimeter + VeConfig.veParameters['stopWord']
            i = i + 1
        return t_flist

    def ConvertRawToLengthTexts(self,messages, delimiter = ' '):
        """
        function: converse messages to n-gram items
        messages: a list of message
        t_lists: str sentence lists
        """
        t_lists = ''
        for message in messages:
            if(len(t_lists) == 0):
                t_lists = t_lists + self.ConvertRawToLengthText(message, delimiter)
            else:
                t_lists = t_lists + '. ' + self.ConvertRawToLengthText(message, delimiter)
        return t_lists

    def filter_words(self, t_dic):
        stop_word = VeConfig.veParameters['stopWord']
        t_words_new = {}
        for key in t_dic:
            if key.find(stop_word) == -1:
                t_words_new[key] = t_dic[key]
        return t_words_new

    def ConvertRawToDict(self, messages):
        """
        function : get frequent of each words
        messages: str multiple sentences
        t_dics: dict words and its frequent
        """
        t_inputs = [self.ConvertRawToLengthTexts(messages)]
        length = VeConfig.veParameters['height'] + 1
        vetorizer = CountVectorizer(ngram_range=(1, length), stop_words=[' ', '.'], token_pattern='(?u)\\b\\w\\w*\\b')
        X = vetorizer.fit_transform(t_inputs)
        t_arrays = np.squeeze(X.toarray())
        words = vetorizer.get_feature_names()
        t_len = len(words)
        t_dics = {}
        i = 0
        while (i < t_len):
            t_dics[words[i]] = int(str(t_arrays[i]))
            i = i + 1
        t_dics = self.filter_words(t_dics)
        self.words_table = t_dics
        prefix = ve_strategy().GetWordsKeys('RawWords')
        if not redis_convert.is_exist_key(prefix):
            redis_convert.insert_to_redis(prefix, t_dics)
        return t_dics

    def ConvertTextToCount(self, message, h):
        fResult = set()
        i = 0
        while(i <= len(message) - h):
            j = i + 1
            while(j < i + h):
                if message[i:j] not in fResult:
                    fResult.add(message[i:j])
                j = j + 1
            i = i + 1
        return fResult

    def ConvertRawToSimDic(self, text, nrange = (1, 1), stopWords = [' ']):
        """
        function : get frequent of each words
        messages: str multiple sentences
        t_dics: dict words and its frequent
        """
        word_cnt = CountVectorizer(ngram_range=nrange, stop_words=stopWords)
        word_result = word_cnt.fit_transform(text)
        word_num = {}
        words = word_cnt.get_feature_names()
        length = len(words)
        word_array = word_result.toarray()
        for j in range(length):
            for i in range(len(word_array)):
                if i == 0:
                    word_num[words[j]] = word_array[i][j]
                else:
                    word_num[words[j]] = word_num[words[j]] + word_array[i][j]
        return word_num

    def convert_text_to_raw(self, phrase):
        pass

    def border2item(self, borders):
        itoms = []
        i = 0
        while(i < len(borders)):
            if i == 0:
                itoms.append((0,borders[i]))
            else:
                itoms.append((borders[i-1],borders[i]))
            i = i + 1
        return itoms

    @staticmethod
    def byteListToHex(byteLists):
        hexList = [hex(x) for x in byteLists]
        return ' '.join(hexList)

    @staticmethod
    def convert_raw_to_count(datas):
        r_wordnum = {}
        for data in datas:
            if data in r_wordnum:
                r_wordnum[data] = r_wordnum[data] + 1
            else:
                r_wordnum[data] = 1
        return r_wordnum

    @staticmethod
    def caculate_prob(vector):
        t_r = {}
        for v in vector:
            if v not in t_r:
                t_r[v] = 1
            else:
                t_r[v] = t_r[v] + 1
        for key in t_r:
            t_r[key] = t_r[key] / len(vector)
        return t_r

    @staticmethod
    def huxinxi(vectorone, vectortwo, vectorthree):
        vectorthree = []
        t_probone = Converter.caculate_prob(vectorone)
        t_probtwo = Converter.caculate_prob(vectortwo)
        t_probsum = Converter.caculate_prob(vectorthree)
        t_info = 0
        for key_one in t_probone:
            for key_two in t_probtwo:
                if key_one + key_two not in t_probsum:
                    continue
                t_info = t_info + t_probsum[key_one + key_two] * np.log(
                    t_probsum[key_one + key_two] / (t_probone[key_one] * t_probtwo[key_two]))
        return t_info

    def ConvertRawToNormalFrequent(self, RawDicts, nrange):
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
        for i in range(1, nrange + 1):
            t_fredic[i] = []
            t_biaozhun[i] = []
        for key in RawDicts:
            t_fredic[len(key.split(' '))].append(RawDicts[key])

        for i in range(1,nrange + 1):
            t_fredic[i] = sum(t_fredic[i])
        t_frer = {}
        for key in RawDicts:
            t_frer[key] = -np.log(RawDicts[key] / t_fredic[len(key.split(' '))])
            t_biaozhun[len(key.split(' '))].append(t_frer[key])
        for i in range(1,nrange + 1):
            print(i, len(t_biaozhun[i]))
            t_mean[i] = np.mean(np.array(t_biaozhun[i]))
            t_std[i] = np.std(np.array(t_biaozhun[i]),ddof = 1)
        for key in RawDicts:
            if t_std[len(key.split(' '))] != 0:
                t_frer[key] = (t_frer[key] - t_mean[len(key.split(' '))]) / t_std[len(key.split(' '))]
            else:
                t_frer[key] = 0
        return t_frer

    def ConvertListToOrder(self, rawlist):
        for item in rawlist:
            item.sort()
        return rawlist

    def ConvertListDicToOrder(self, rawlist):
        LS = []
        for item in rawlist:
            LS.append(sorted(item.items(),key=lambda x:x[0]))
        return LS

    def MergeLists(self, ListA, ListB):
        s_los = set()
        for key in ListA:
            s_los.add(key)
        for key in ListB:
            s_los.add(key)
        l_los = list(s_los)
        l_los.sort()
        return l_los

    def MergeListGroup(self, ListsA, ListsB):
        i = 0
        MergeBorders = []
        for i in range(len(ListsA)):
            tempBorder = Converter().MergeLists(ListsA[i], ListsB[i])
            MergeBorders.append(tempBorder)
        return MergeBorders
    """
    Convert byte to int
    """
    @staticmethod
    def byteToBigInt(data):
        return int.from_bytes(data, byteorder='big', signed=False)

    @staticmethod
    def byteToLittle(data):
        return int.from_bytes(data, byteorder='little', signed=False)

    @staticmethod
    def bytesToBigInt(datas):
        return [Converter.byteToBigInt(data) for data in datas]

    @staticmethod
    def bytesToLittleInt(datas):
        return [Converter.byteToLittle(data) for data in datas]

    def MergeDicts(self, dicOne, dicTwo):
        for key in dicOne:
            if key not in dicTwo:
                dicTwo[key] = dicOne[key]
            else:
                dicTwo[key] = dicTwo[key] + dicOne[key]
        return dicTwo

    def MergeListDics(self, listDics):
        mergedDic = {}
        for listDic in listDics:
            mergedDic = self.MergeDicts(mergedDic, listDic)
        return mergedDic

    def ConvertListToCnt(self, datas, h):
        fDics = {}
        for data in datas:
            tempCnt = self.ConvertTextToCount(data, h)
            for key in tempCnt:
                if key not in fDics:
                    fDics[key] = 0
                fDics[key] = fDics[key] + 1
        return fDics

    def ConvertMultiList(self, Datas):
        for data in Datas:
            if isinstance(data, list):
                yield self.ConvertMultiList(data)
            else:
                yield Datas
                break

    def getDatasByLocs(self, messages, los):
        losMessages = []
        for message in messages:
            if len(message) > los[-1]:
                losMessages.append(message[los[0]:los[1]])
        return losMessages

    def ConvertMultiListPure(self, Datas, finalResult):
        for data in Datas:
            if isinstance(data, list):
                self.ConvertMultiListPure(data, finalResult)
            else:
                finalResult.append(Datas)
                break

word_converter = Converter()

if __name__ == '__main__':
    counter = Converter()
    #raw_words = redis_convert.read_from_redis(raw_keys)
    #frequent_words = Converter().ConvertRawToNormalFrequent(raw_words, ve_strategy().vote_parameters['height'] + 1)
    datas = read_datas('/home/wxw/data/iec104', 'single')
    datas = get_puredatas(datas)
    counter.ConvertRawToDict(datas)
    #datas = read_datas('/home/wxw/data/modbustest', 'single')
    #datas = get_puredatas(datas)
    #datas = get_data_bylo(datas, 2, 5)
    #datas = counter.convert_raw_to_count(datas)
    #print(datas)



