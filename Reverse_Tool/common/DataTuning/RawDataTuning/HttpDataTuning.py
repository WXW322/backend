from common.readdata import *
from common.Converter.MessageConvert import MessageConvert
from textops.TextParseLogic import TextParseLogic
import sys

class HttpDataTuning:
    def __init__(self):
        pass

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


    def tuningHttpBydire(self):
        messages = read_datas('/home/wxw/data/httpDatas/http', 'single')
        messages = get_puredatas(messages)
        messages = MessageConvert.filterMsgs(['GET', 'POST', 'HTTP'], messages, 10)
        clsMessages = MessageConvert.clsMessagesByRegix(['GET', 'POST'], 5, messages)
        clsDesMessages = clsMessages['unkown']
        message_parser = TextParseLogic()
        desDatas = message_parser.ConvertDataToMessage(clsDesMessages, b'\r\n')
        desNowDatas = [datanow.now() for datanow in desDatas]
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
        messages = MessageConvert.filterMsgs(['GET', 'POST', 'HTTP'], messages, 10)
        clsMessages = MessageConvert.clsMessagesByRegix(['GET', 'POST'], 5, messages)
        srcDatas = []
        desDatas = []
        i = 0
        srcDatas.extend(clsMessages['GET'])
        srcDatas.extend(clsMessages['POST'])
        desDatas.extend(clsMessages['unkown'])
        return srcDatas, desDatas



if __name__ == '__main__':
    httpDataTuning = HttpDataTuning()
    httpDataTuning.tuningHttpDatasTotal()
    #httpDataTuning.tuningTwoHttpBydire()