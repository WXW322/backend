
import sys
from netzob.all import *
from common.readdata import *
from textops.Model.TextModel import TextModel

class TextParseLogic:
    def __init__(self):
        self.name = 'parser'

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


if __name__ == '__main__':
    message_parser = TextParseLogic()
    messages = read_datas('/home/wxw/data/httpDatas/http_small', 'single')
    messages = get_puredatas(messages)
    datas = message_parser.ConvertDataToMessage(messages, b'\r\n')
    print(datas[0].now(3))