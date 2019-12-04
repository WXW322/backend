from common.readdata import *
from common.Converter.MessageConvert import MessageConvert
from textops.TextParseLogic import TextParseLogic
import sys

class HttpDataTuning:
    def __init__(self):
        self.cmds = [b'GET', b'POST', b'HEAD', b'HTTP/1.1 200',
                     b'HTTP/1.1 302', b'HTTP/1.0 200', b'HTTP/1.1 404',
                     b'HTTP/1.1 304', b'HTTP/1.1 301',
                     b'HTTP/1.1 502']

    def tuningTwoHttpBydire(self):
        srcData, desData = self.tuningHttpByregix()
        message_parser = TextParseLogic()
        desDatas = message_parser.ConvertDataToMessage(desData, b'\r\n')
        desNowDatas = [datanow.now() for datanow in desDatas]
        diff = {}
        for desNow in desNowDatas:
            if desNow not in diff:
                diff[desNow] = 1
            else:
                diff[desNow] = diff[desNow] + 1
        print(diff)

    def getRawDatas(self):
        messages = read_datas('/home/wxw/data/httpDatas/http', 'single')
        messages = get_puredatas(messages)
        messages = self.filterMsgs(messages, b'\r\n')
        return messages

    def getDiffDatas(self, datas):
        desNowDatas = [datanow.now() for datanow in datas]
        diff = {}
        for desNow in desNowDatas:
            if desNow not in diff:
                diff[desNow] = 1
            else:
                diff[desNow] = diff[desNow] + 1
        print(diff)

    def filterMsgs(self, messages, delimiter):
        newMsgs = []
        for message in messages:
            if message.find(delimiter) != -1:
                newMsgs.append(message[0:15])
        return newMsgs

    def getTotalDatas(self, messages):
        message_parser = TextParseLogic()
        messages = message_parser.ConvertDataToMessage(messages, b'\r\n')
        self.getDiffDatas(messages)



    def tuningHttpDatasTotal(self):
        srcData, desData = self.tuningTotol()
        totalDatas = []
        totalDatas.extend(srcData)
        totalDatas.extend(desData)
        message_parser = TextParseLogic()
        desDatas = message_parser.ConvertDataToMessage(desData, b'\r\n')
        desNowDatas = [datanow.now() for datanow in desDatas]
        #desNowDatas = [str(datanow.now()).split(' ')[0] for datanow in desDatas]
        diff = {}
        for desNow in desNowDatas:
            if desNow not in diff:
                diff[desNow] = 1
            else:
                diff[desNow] = diff[desNow] + 1
        print(diff)




    def tuningHttpBydire(self, tPath='/home/wxw/data/httpDatas/http'):
        messages = read_datas(tPath, 'single')
        messages = MessageConvert.filterMsgs(['GET', 'POST', 'HTTP', 'HEAD'], messages, 10)
        clsMessages = MessageConvert.clsMessagesByRegix(['GET', 'POST', 'HEAD'], 5, messages)
        clsDesMessages = clsMessages['unkown']
        srcDatas = []
        srcDatas.extend(clsMessages['GET'])
        srcDatas.extend(clsMessages['POST'])
        srcDatas.extend(clsMessages['HEAD'])
        message_parser = TextParseLogic()
        #desDatas = message_parser.ConvertDataToMessage(clsDesMessages, b'\r\n')
        desDatas = message_parser.ConvertDataToMessage(srcDatas, b'\r\n')
        #desNowDatas = [datanow.now() for datanow in desDatas]
        desNowDatas = [datanow.now().split(b' ')[0] for datanow in desDatas]
        diff = {}
        for desNow in desNowDatas:
            if desNow not in diff:
                diff[desNow] = 1
            else:
                diff[desNow] = diff[desNow] + 1
        print(diff)

    def tuningHttpByregix(self):
        messages = read_datas('/home/wxw/data/httpDatas/http', 'single')
        messages = get_puredatas(messages)
        messages = MessageConvert.filterMsgs(['GET', 'POST', 'HTTP'], messages, 10)
        clsMessages = MessageConvert.clsMessagesByRegix(['GET', 'POST'], 5, messages)
        srcDatas = []
        desDatas = []
        i = 0
        while (i < 252):
            srcDatas.append(clsMessages['GET'][i])
            srcDatas.append(clsMessages['POST'][i])
            i = i + 1
        desDatas.extend(clsMessages['unkown'])
        desDatas = desDatas[0:505]
        return srcDatas, desDatas

    def tuningTotol(self):
        messages = read_datas('/home/wxw/data/httpDatas/http', 'single')
        messages = get_puredatas(messages)
        messages = MessageConvert.filterMsgs(['GET', 'POST', 'HTTP', 'HEAD'], messages, 10)
        clsMessages = MessageConvert.clsMessagesByRegix(['GET', 'POST', 'HEAD'], 5, messages)
        srcDatas = []
        desDatas = []
        i = 0
        srcDatas.extend(clsMessages['GET'])
        srcDatas.extend(clsMessages['POST'])
        desDatas.extend(clsMessages['unkown'])
        return srcDatas, desDatas

    def getTotalData(self):
        datas = self.getRawDatas()
        datasSplit = MessageConvert.clsMsgsByRegix(self.cmds, 20, datas)
        return datasSplit

    def sampleDatas(self):
        datas = self.getTotalData()
        Fdatas = []
        for key in datas:
            print(key, len(datas[key]))
            if len(datas[key]) > 2000:
                print('zzz')
                Fdatas.extend(datas[key][0:2000])
            else:
                Fdatas.extend(datas[key])
        print(len(Fdatas))
        return Fdatas

    def getMsgsLen(self, clses):
        correLen = 0
        conciouLen = 0
        print(len(clses))
        clsCmds = []
        for cls in clses:
            clsCmd = MessageConvert.clsMsgsByRegix(self.cmds, 20, cls)
            clsCmds.append(clsCmd)
        for clscmd in clsCmds:
            if len(clscmd) == 1:
                correLen = correLen + 1
        for cmd in self.cmds:
            tLo = 0
            for clscmd in clsCmds:
                if cmd in clscmd:
                    tLo = tLo + 1
            if tLo == 1:
                conciouLen = conciouLen + 1
        print(correLen, conciouLen)





if __name__ == '__main__':
    httpDataTuning = HttpDataTuning()
    sdatas = httpDataTuning.sampleDatas()
    #httpDataTuning.getMsgsLen(sdatas)
    #httpDataTuning.tuningHttpBydire()
    #httpDataTuning.getTotalData()
    #httpDataTuning.getTotalDatas()
    #httpDataTuning.tuningHttpDatasTotal()
    #httpDataTuning.tuningTwoHttpBydire()