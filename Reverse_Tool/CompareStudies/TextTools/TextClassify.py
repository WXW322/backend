
from LDA.lad import *
from common.Converter.base_convert import Converter
from common.Merger.WordsMerger import WordsMerger
from common.analyzer.analyzer_common import base_analyzer
from common.DataTuning.FeatureGenerate.WordsFGene import WordsFeatureGene
from common.Classify.Kmeans import KmeansClasser
from common.Classify.Dbscan import DbScanClasser
import sys

class TextClassify:
    def __init__(self, messages):
        self.messages = messages
        self.cVerTer = Converter()
        self.freWords = {}
        self.mger = WordsMerger()
        self.analyzer = base_analyzer()
        self.features = None

    def merGeWords(self, freWords):
        comBineFreWords = []
        for words in freWords:
            words = [word.split('_') for word in words]
            comBineFreWords.append(self.mger.mergeWords(words))
        return comBineFreWords

    def cntWord(self, wSize, TK, wLen):
        freWords,_ = get_messages(self.messages, wSize, TK, wLen)
        wSetv = set()
        for freWordList in freWords:
            for word in freWordList:
                if word not in self.freWords:
                    wSetv.add(word)
        textList = self.cVerTer.ConvertRawToLengthTexts(self.messages, '_')
        for word in wSetv:
            self.freWords[word] = textList.count(word)
        return self.freWords

    def cntPro(self, words=None):
        if words == None:
            self.freWords = self.analyzer.convert_num_to_frequent(self.freWords)
        else:
            self.freWords = self.analyzer.convert_num_to_frequent(words)
        return self.freWords

    def FeGenerator(self):
        tulWords = [word for word in self.freWords.items()]
        featureGene = WordsFeatureGene(tulWords)
        textMsgs = [self.cVerTer.ConvertRawToLengthText(message, delimeter='_') for message in self.messages]
        mFeatures = featureGene.cvtMsgs(textMsgs)
        self.features = mFeatures
        return mFeatures

    def clsMessages(self, wSize, TK, wLen, Kcls):
        self.cntWord(wSize, TK, wLen)
        self.cntPro()
        wFeatures = self.FeGenerator()
        clser = KmeansClasser()
        return clser.clsMessages(self.messages, wFeatures, Kcls)

    def clsByDbscan(self, wSize, TK, wLen, mindis, minpt):
        self.cntWord(wSize, TK, wLen)
        self.cntPro()
        wFeatures = self.FeGenerator()
        clser = DbScanClasser()
        return clser.clsMessages(self.messages, wFeatures, mindis, minpt)







