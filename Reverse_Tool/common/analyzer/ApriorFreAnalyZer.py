
from common.analyzer.BaseFreAnalyZer import BaseFreAnalyZer
import sys
import time

class ApriorFreAnalyZer(BaseFreAnalyZer):
    def __init__(self, texts, supportRate):
        super().__init__(texts)
        self.freTextSet = set()
        self.support = supportRate
        self.freTexts = []

    def genStr(self):
        seNew = set()
        for i in range(0, len(self.freTexts)):
            for j in range(0, len(self.freTexts)):
                textNew = self.freTexts[i] + self.freTexts[j]
                if textNew not in self.freTextSet and textNew not in seNew:
                    seNew.add(textNew)
        return seNew

    def genInitSingle(self):
        tempTextSet = set()
        for s in self.texts:
            if s not in tempTextSet:
                tempTextSet.add(s)
        return tempTextSet

    def genInitSet(self):
        tempTextSet = set()
        for text in self.texts:
            for s in text:
                if s not in tempTextSet:
                    tempTextSet.add(s)
        return tempTextSet

    # Compare study
    def filterSe(self, sequences):
        tempSet = set()
        for se in sequences:
            tempSupport = self.getWordsCount(se)
            if tempSupport / self.getTextLength(len(se)) >= self.support and se not in tempSet:
                tempSet.add(se)
        return tempSet

    def filterSeBySet(self, sequences):
        tempSet = set()
        for se in sequences:
            tempSupport = self.geSetWordsCount(se)
            #print(se, tempSupport)
            if tempSupport / self.getTextLengthSet(len(se)) >= self.support and se not in tempSet:
                tempSet.add(se)
        return tempSet

    def filterSeByCnt(self, sequences):
        tempSet = set()
        for se in sequences:
            tempSupport = self.getTextCnt(se)
            if tempSupport / len(self.texts) >= self.support and se not in tempSet:
                tempSet.add(se)
        #print(tempSet)
        return tempSet



    def updateSet(self, newDatas):
        for data in newDatas:
            if data not in self.freTextSet:
                self.freTexts.append(data)
                self.freTextSet.add(data)

    def filterShort(self):
        for i in range(len(self.freTexts)):
            for j in range(len(self.freTexts)):
                if len(self.freTexts[j]) > len(self.freTexts[i]) and self.freTexts[j].find(self.freTexts[i]) != -1:
                    if self.freTexts[i] in self.freTextSet:
                        self.freTextSet.remove(self.freTexts[i])

    def getApriorFre(self):
        tempTextSet = self.genInitSet()
        self.updateSet(self.filterSeByCnt(list(tempTextSet)))
        while(True):
            startTime = time.time()
            newDatas = self.genStr()
            endTime = time.time()
            print('The generate time is %d %d %s'%(len(self.freTexts), len(newDatas), str(endTime - startTime)))
            nowSe = self.filterSeByCnt(newDatas)
            endTime = time.time()
            print('The filter time is %d %s' % (len(nowSe), str(endTime - startTime)))
            if(len(nowSe) == 0):
                break
            else:
                self.updateSet(nowSe)
            if len(self.freTextSet) >1500:
                break
        self.filterShort()
        return self.freTextSet

if __name__ == '__main__':
    aprior = ApriorFreAnalyZer(['GET sadasd', 'GET kkjjll', 'POST jjkslasm', 'POST xoxixo'], 0.2)
    print(aprior.getApriorFre())

