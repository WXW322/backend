
import abc

class BaseFreAnalyZer(metaclass=abc.ABCMeta):
    def __init__(self, texts):
        self.texts = texts


    def getWordsCount(self, textNow):
        cnt = self.texts.count(textNow)
        return cnt

    def geSetWordsCount(self, textNow):
        cnt = 0
        for text in self.texts:
            cnt = cnt + text.count(textNow)
        return cnt

    def getTextLength(self, h):
        return len(self.texts) - h - 1

    def getTextLengthSet(self, h):
        length = 0
        for text in self.texts:
            length = length + len(text) - h - 1
        return length

    def getTextCnt(self, textNow):
        cnt = 0
        for text in self.texts:
            if text.find(textNow) != -1:
                cnt = cnt + 1
        return cnt








