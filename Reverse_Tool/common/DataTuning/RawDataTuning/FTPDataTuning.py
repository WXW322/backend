from common.readdata import *
from common.Converter.MessageConvert import MessageConvert
from textops.TextParseLogic import TextParseLogic

class FTPDataTuning:
    def __init__(self):
        pass

    def tuningTwoHttpBydire(self):
        srcData, desData = self.tuningHttpByregix()
        message_parser = TextParseLogic()
        desDatas = message_parser.ConvertDataToMessage(srcData, b'\r\n')
        desNowDatas = [datanow.now() for datanow in desDatas]
        diff = {}
        for desNow in desNowDatas:
            #desNow = str(desNow).split(' ')[0]
            desNow = str(desNow)
            lo = desNow.find('(')
            if lo != -1:
                desNow = desNow[0:lo]
            lo = desNow.find('/')
            if lo != -1:
                desNow = desNow[0:lo]
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
        datas = read_datas('/home/wxw/data/ftp/ftpData', 'multy')
        datasF = []
        for data in datas:
            if len(data) < 100:
                datasF.extend(data)
            else:
                datasF.extend(data[0:500])
        srcDatasF, desDatasF = MessageConvert.clsMessageByDire(datasF)
        srcDatasF = get_puredatas(srcDatasF)
        desDatasF = get_puredatas(desDatasF)
        print(len(desDatasF))
        return srcDatasF, desDatasF


if __name__ == '__main__':
    ftptuning = FTPDataTuning()
    ftptuning.tuningTwoHttpBydire()