
import sys
from netzob.all import *
from common.readdata import *
from textops.Model.TextModel import TextModel
from common.Spliter.MsgSpliter import MsgSpliter

class TextParseLogic:
    def __init__(self):
        self.name = 'parser'
        self.msgSpliter = MsgSpliter()

    def split(self, messages, delimiter):
        t_messages = []
        for message in messages:
            t_messages.append(message.split(delimiter))
        return t_messages

    def ConvertDataToMessage(self, messages, delimeter, h = 0):
        textDatas = []
        splitDatas = self.split(messages, delimeter)
        i = 0
        while(i < len(messages)):
            textModel = TextModel(messages[i], splitDatas[i], i, h)
            textDatas.append(textModel)
            i = i + 1
        return textDatas

    def spltMsgs(self, messages, delimiter):
        spltmsgs = []
        for message in messages:
            spltmsgs.append([str(itom) for itom in message.split(delimiter)])
        headers = []
        for i in range(6):
            if i % 2 != 0:
                headers.append('field' + str(i))
            else:
                headers.append(str(delimiter))
        return headers, spltmsgs

    def spltMsgsSimple(self, messages, delimiter, maxRange=150):
        spltmsgs = []
        for message in messages:
            spltmsgs.append(message.split(delimiter))
        return self.msgSpliter.splitTextMsgs(spltmsgs, delimiter, maxRange)



if __name__ == '__main__':
    message_parser = TextParseLogic()
    messages = read_datas('/home/wxw/data/httpDatas/http_small', 'single')
    messages = get_puredatas(messages)
    h, D = message_parser.spltMsgs(messages, b'\r\n')
    print(h)
    print(D)
    #datas = message_parser.ConvertDataToMessage(messages, b'\r\n')
    #print(datas[0].now(3))