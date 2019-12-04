

from sklearn.feature_extraction.text import CountVectorizer
import re
from common.readdata import *
from common.Converter.base_convert import Converter
from sklearn.feature_extraction.text import TfidfTransformer
from common.analyzer.analyzer_common import base_analyzer
from common.DataTuning.RawDataTuning.HttpDataTuning import HttpDataTuning
import sys

analyzer = base_analyzer()
def get_ngram_words(text, nrange = (1, 1), topk = 1):
    word_cnt = CountVectorizer(ngram_range=nrange, stop_words=[' '])
    word_result = word_cnt.fit_transform(text)
    word_num = {}
    words = word_cnt.get_feature_names()
    length = len(words)
    word_array = word_result.toarray()[0]
    for i in range(length):
        word_num[words[i]] = word_array[i]
    words_result = rank_word(word_num, text[0])
    words_result = [word[0] for word in words_result[0:topk]]
    return words_result


def get_pure_word(words_result):
    while(len(words_result) > 0):
        start = words_result[0]
        j = 1
        t_lo = 0
        while(j < len(words_result)):
            if(words_result[j].find(start) != -1):
                del words_result[0]
                t_lo = 1
                break
            j = j + 1
        if(t_lo == 0):
            break
    return words_result[0]




def get_TF_idf(text, nrange = (1, 1)):
    vectorizer = CountVectorizer(ngram_range=nrange, stop_words=[' '])
    # 计算个词语出现的次数
    X = vectorizer.fit_transform(text)
    # 获取词袋中所有文本关键词
    word = vectorizer.get_feature_names()
    print(word)
    transformer = TfidfTransformer()
    print(transformer)
    # 将词频矩阵X统计成TF-IDF值
    tfidf = transformer.fit_transform(X)
    # 查看数据结构 tfidf[i][j]表示i类文本中的tf-idf权重
    print(tfidf.toarray())

def is_unseen_words(words):
    #print('before: ' + words)
    ches = words.split(' ')
    #print(ches)
    for ch in ches:
        if int(ch) > 41:
            return False
    return True


def get_dis_score(start, end, cnt):
    return (end - start + 1) / cnt

def filterWords(words):
    '''
    :param words:[(word, num)]
    :return: str
    '''
    rWords = set()
    for word in words:
        if word[0] not in words:
            rWords.add(word[0])
    i = 0
    print(rWords)
    uniwords = []
    deliword = None
    while(i < len(words) - 1):
        if words[i][0] not in rWords:
            continue
        j = 0
        isUnique = True
        while(j < len(words)):
            if (len(words[j][0]) > len(words[i][0]) and words[j][0].find(words[i][0]) != -1):
                isUnique = False
                break
            j = j + 1
        if(isUnique):
            uniwords.append(words[i][0])
            if deliword == None:
                deliword = words[i][0]
        i = i + 1
    print(uniwords)
    return deliword

def filterFieldWords(words):
    '''
      :param words:[(word, num)]
      :return: str
      '''
    print(words)
    uniwords = []
    deliword = None
    i = 0
    while (i < len(words) - 1):
        j = 0
        isUnique = True
        while (j < len(words)):
            if (len(words[j]) > len(words[i]) and words[j].find(words[i]) != -1):
                isUnique = False
                break
            j = j + 1
        if (isUnique):
            uniwords.append(words[i])
            if deliword == None:
                deliword = words[i]
        i = i + 1
    print(uniwords)
    return deliword

def rank_word(word_cnt, text):
    words_score = []
    Tcnt = sum([word_cnt[word] for word in word_cnt])
    for word in word_cnt:
        start = text.find(word)
        end = text.rfind(word)
        words_score.append((word, get_dis_score(start, end, Tcnt)))
        #words_score.append((word, get_dis_score(start, end, word_cnt[word])))
    words_score = sorted(words_score, key = lambda x: x[1], reverse=True)
    words_result = []
    tLo = -1
    for word in words_score:
        if is_unseen_words(word[0]):
            words_result.append(word)
            tLo = 0
    if tLo == -1:
        words_result.extend([word for word in words_score])
    return words_result

def getDelimiter(datas):
    convert = Converter()
    messages = [convert.convert_raw_to_text(data) for data in datas]
    t_results = []
    for message in messages:
        t_results.extend(get_ngram_words([message], (1, 2), 10))
    words = analyzer.get_topk(t_results)[0:10]
    print(words)
    deliWords = filterWords(words)
    wordsList = [chr(int(word)) for word in deliWords.split(' ')]
    deliW = ''.join(wordsList)
    return deliW, deliWords

if __name__ == '__main__':
    """
    datas = read_datas('/home/wxw/data/httpDatas/http_test', 'single')
    print(len(datas))
    datas = get_puredatas(datas)
    """
    httpDatatuning = HttpDataTuning()
    src, des = httpDatatuning.tuningHttpByregix()
    datas= []
    datas.extend(src)
    datas.extend(des)
    print(getDelimiter(datas))