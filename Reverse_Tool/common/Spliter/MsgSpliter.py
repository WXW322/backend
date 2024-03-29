
from common.Converter.base_convert import Converter
from common.readdata import *
import sys

class MsgSpliter:
    def __init__(self):
        pass

    def splitMessage(self, boundary, message, maxRange):
        hexData = Converter.byteListToHex(message)
        splitMsg = ''
        los = 0
        startLo = 0
        hexDatas = hexData.split(' ')
        if boundary[los] == 0:
            los = los + 1
        for i in range(min(len(hexDatas), maxRange)):
            if los >= len(boundary):
                splitMsg = splitMsg + hexDatas[i] + ' '
                continue
            splitMsg = splitMsg + hexDatas[i] + ' '
            if i + 1 == boundary[los]:
                splitMsg = splitMsg + '|'
                los = los + 1
        return splitMsg

    def splitMessages(self, boundaries, messages, maxRange=15):
        splitMsgs= []
        for i in range(len(boundaries)):
            splitMsgs.append(self.splitMessage(boundaries[i], messages[i], maxRange))
        return splitMsgs

    def splitMessageByType(self, boundary, message):
        hexData = Converter.byteListToHex(message)
        splitMsg = ''
        los = 0
        spltMsgs = []
        hexDatas = hexData.split(' ')
        if boundary[los] == 0:
            los = los + 1
        for i in range((len(hexDatas))):
            if los >= len(boundary):
                splitMsg = splitMsg + hexDatas[i] + ' '
                continue
            splitMsg = splitMsg + hexDatas[i] + ' '
            if i + 1 == boundary[los]:
                spltMsgs.append(splitMsg)
                splitMsg = ''
                los = los + 1
        return spltMsgs

    def splitMsgByTypes(self, boundaries, messages):
        splitMsgs = []
        for i in range(len(boundaries)):
            splitMsgs.append(self.splitMessageByType(boundaries[i], messages[i]))
        return splitMsgs

    def splitTextMsgs(self, msgs, delimiter, maxRange=150):
        spltMsgs = []
        print(msgs[0])
        for msg in msgs:
            textMsg = ''
            for itom in msg:
                textMsg = textMsg + str(itom) + ' | | | ' + str(delimiter) + ' | | | '
            spltMsgs.append(textMsg[0:maxRange])
        print(spltMsgs[0])
        return spltMsgs


if __name__ == '__main__':
    messages = read_datas('/home/wxw/data/ToolDatas/15895903730.10.222', 'single')
    messages = get_puredatas(messages)
    msgSpliter = MsgSpliter()
    print(msgSpliter.splitMessages([[1,2,5,7],[1,2,3,6]], [messages[0], messages[1]]))




