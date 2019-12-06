
import time
from textops.Model.TextModel import TextModel
from common.analyzer.ApriorFreAnalyZer import ApriorFreAnalyZer
from textops.DelimiterFindLogic import *
from textops.TextParseLogic import TextParseLogic
import sys
from common.RanKer.BaseRankModel import BaseRankModel
from common.Converter.base_convert import Converter
from common.DataTuning.RawDataTuning.HttpDataTuning import HttpDataTuning
from common.DataTuning.RawDataTuning.FTPDataTuning import FTPDataTuning
from common.DataTuning.RawDataTuning.RedisDataTuning import RedisDataTuning

class TextClassifyLogic:
    def __init__(self, messages, tRate, sRate, wRate, wHeight):
        self.tRate = tRate
        self.srate = sRate
        self.wRate = self.srate
        self.wHeight = wHeight
        self.messages = messages
        self.httpData = HttpDataTuning()
        self.ftpData = FTPDataTuning()
        self.redisData = RedisDataTuning()

    def GetLocData(self, datas):
        nowLocData = []
        for data in datas:
            nowLocData.append(data.now())
        return nowLocData

    def filterShort(self, freWords, h):
        newFreWords = set()
        for value in freWords:
            if(len(value) >= h):
                newFreWords.add(value)
        return newFreWords

    def GetFrequentWords(self, rate, h, datas):
        nowLocDatas = self.GetLocData(datas)
        Datas = [str(data) for data in nowLocDatas]
        freWords = ApriorFreAnalyZer(Datas, rate).getApriorFre()
        freWords = self.filterShort(freWords, h)
        return freWords

    def RankWord(self, word, datas):
        nowLocDatas = self.GetLocData(datas)
        Datas = [str(data) for data in nowLocDatas]
        cnt = 0
        loc = 0
        for data in Datas:
            tempLoc = data.find(word)
            if tempLoc != -1:
                cnt = cnt + 1
                loc = loc + tempLoc
        print(word, cnt, loc)
        return(cnt, (loc + 1) / cnt)

    def RankWords(self, freWords, datas):
        words = []
        for freWord in freWords:
            nums = self.RankWord(freWord, datas)
            words.append((freWord, nums[0], nums[1]))
        words = BaseRankModel.sortList(words)
        return words

    def ConvertFreWords(self, data):
        freSet = {}
        for freWord in self.freWords:
            lo = data.find(freWord)
            if lo != -1:
                freSet[freWord] = lo
        frePattern = sorted(freSet.items(), key=lambda key:key[1])
        finalPattern = ''.join([item[0] for item in frePattern])
        return finalPattern

    def GetWodsRank(self, datas):
        freWords = self.GetFrequentWords(self.wRate, self.wHeight, datas)
        rankWords = self.RankWords(freWords, datas)
        return rankWords

    def ClassifyMessages(self, messages):
        msgSet = {}
        for message in messages:
            freWord = self.ConvertFreWords(str(message.message))
            if freWord not in msgSet:
                msgSet[freWord] = []
            msgSet[freWord].append(message)
        return msgSet

    def ClassifyCircleLy(self, preWords, messages):
        rankWords = self.GetWodsRank(messages)
        funCode = None
        for word in rankWords:
            if word not in preWords and word[1] / len(self.messages) > self.tRate and word[1] != len(self.messages):
                funCode = word
                break
        fResult = []
        print(funCode)
        #if funCode is not None and funCode[1] / len(messages) > self.trate:
        if funCode is not None:
            clsOne, clsTwo = self.ClassifyByCodes(funCode[0], messages)
            print(len(clsOne), len(clsTwo))
            if len(clsTwo) / len(self.messages) > self.tRate:
                fResult.append(self.ClassifyCircleLy(preWords, clsTwo))
            else:
                if len(clsTwo) > 0:
                    fResult.append(clsTwo)
            if len(clsOne) / len(self.messages) > self.tRate:
                preWords.add(funCode)
                fResult.append(self.ClassifyCircleLy(preWords, clsOne))
                preWords.remove(funCode)
            else:
                fResult.append(clsOne)
        else:
            fResult = messages
        return fResult


    def ClassifyByCodes(self, codes, messages):
        clsTwo = []
        clsOne = []
        for message in messages:
            value = str(message.now())
            if value.find(codes)!= -1:
                clsOne.append(message)
            else:
                clsTwo.append(message)
        return (clsOne, clsTwo)


    def FormatInfer(self, rate, h):
        self.GetFrequentWords(rate, h)
        messageClassify = self.ClassifyMessages(self.datas)
        finalFormats = []
        formatInfer = Format()
        for key,value in messageClassify.items():
            tMessages = []
            for message in value:
                singleMessage = RawMessage(message.message)
                tMessages.append(singleMessage)
            tempFormat = Symbol(messages=tMessages)
            formatInfer.splitAligned(tempFormat, doInternalSlick=True)
            finalFormats.append(tempFormat)
        return finalFormats

    def FormatInferCirclely(self, messages, Mtype):
        preFre = set()
        #result = textClassify.classifyMessages(preFre, messages)
        result = self.classifyMessages(preFre, messages)
        clsResult = []
        for res in result:
            clsr = []
            for msg in res:
                clsr.append(msg.message)
            clsResult.append(clsr)
        if Mtype == 'H':
            self.httpData.getMsgsLen(clsResult)
        elif Mtype == 'F':
            self.ftpData.getMsgsLen(clsResult)
        else:
            self.redisData.getMsgsLen(clsResult)
        #httpTuning = HttpDataTuning()
        #print(httpTuning.getMsgsLen(clsResult))
        #ftpTuning = FTPDataTuning()
        #print(ftpTuning.getMsgsLen(clsResult))
        #redisTuning = RedisDataTuning()
        #redisTuning.getMsgsLen(clsResult)
        finalFormats = []
        formatInfer = Format()
        for dataList in result:
            tMessages = []
            for data in dataList:
                singMessage = RawMessage(data.message)
                tMessages.append(singMessage)
            tempFormat = Symbol(messages=tMessages)
            formatInfer.splitAligned(tempFormat, doInternalSlick=True)
            finalFormats.append(tempFormat)
        return finalFormats



    def filterSets(self, result, fResult):
        cverter = Converter()
        cverter.ConvertMultiListPure(result, fResult)

    def classifyMessages(self, preSet, messages):
        datas = self.ClassifyCircleLy(preSet, messages)
        result = []
        self.filterSets(datas, result)
        return result


if __name__ == '__main__':
    beginTime = time.time()
    messages = read_datas('/home/wxw/data/httpDatas/http_measure', 'single')
    messages = get_puredatas(messages)
    print(len(messages))
    message_parser = TextParseLogic()
    messages = message_parser.ConvertDataToMessage(messages, b'\r\n')
    textClassify = TextClassifyLogic(messages, 0.1, 0.4, 0.2, 3)
    fFormats = textClassify.FormatInferCirclely(messages)
    for f in fFormats:
        print(f.getLeafFields)
    #textClassify.GetFrequentWords(0.3, 3)
    #print(textClassify.GetWodsRank(messages))
    #msgSet = textClassify.FormatInfer(0.3, 3)
    #for value in msgSet:
    #    print(value._str_debug())
    #endTime = time.time()
    #print(endTime - beginTime)