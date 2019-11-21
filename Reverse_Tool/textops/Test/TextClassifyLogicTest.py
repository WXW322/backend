
from textops.TextClassifyLogic import TextClassifyLogic
from common.readdata import *
from textops.TextParseLogic import TextParseLogic
from common.Converter.MessageConvert import MessageConvert
from common.DataTuning.RawDataTuning.HttpDataTuning import HttpDataTuning
from common.DataTuning.RawDataTuning.FTPDataTuning import FTPDataTuning
import sys

class TextClassifyLogicTest:
    def __init__(self, messages, srate, rrate, trate, h):
        self.textcls = TextClassifyLogic(messages, srate, rrate, trate, h)

    def FormatInferCirclelyTest(self, messages):
        fFormats = self.textcls.FormatInferCirclely(messages)
        for f in fFormats:
            print(f._str_debug())

    def getHeadAndNum(self, messages):
        datas = self.textcls.GetLocData(self.textcls.messages)
        hNums = {}
        for hdata in datas:
            cc = str(hdata).split(' ')[0]
            if cc not in hNums:
                hNums[cc] = 1
            else:
                hNums[cc] = hNums[cc] + 1
        print(hNums)

    def ftpTest(self, DirPath):
        datas = read_datas(DirPath, 'multy')
        datasF = []
        for data in datas:
            if len(data) < 100:
                datasF.extend(data)
            else:
                datasF.extend(data[0:500])
        srcDatasF, desDatasF = MessageConvert.clsMessageByDire(datasF)
        srcdatas = get_puredatas(srcDatasF)
        desdatas = get_puredatas(desDatasF)
        message_parser = TextParseLogic()
        srcmessages = message_parser.ConvertDataToMessage(srcdatas, b'\r\n')
        desmessages = message_parser.ConvertDataToMessage(desdatas, b'\r\n')
        srctextcls = TextClassifyLogicTest(srcmessages, 0.2, 0.3, 0.4, 3)
        # srctextcls.FormatInferCirclelyTest(srcmessages)
        destextcls = TextClassifyLogicTest(desmessages, 0.1, 0.1, 0.1, 3)
        # destextcls.getHeadAndNum(desmessages)
        destextcls.FormatInferCirclelyTest(desmessages)
        # destextcls = TextClassifyLogicTest(desmessages, 0.1, 0.1, 0.1, 3)
        # textcls.getHeadAndNum(messages)
        # textcls.FormatInferCirclelyTest(messages)

    def httpTest(self, DirPath):
        datas = read_datas(DirPath, 'multy')
        print(len(datas))




if __name__ == '__main__':
    message_parser = TextParseLogic()
    #httptuning = HttpDataTuning()
    #srcDatas, desDatas = httptuning.tuningHttpByregix()
    ftpTuning = FTPDataTuning()
    srcDatas, desDatas = ftpTuning.tuningHttpByregix()
    desmessages = message_parser.ConvertDataToMessage(desDatas, b'\r\n')
    destextcls = TextClassifyLogicTest(desmessages, 0.05, 0.2, 0.2, 3)
    destextcls.FormatInferCirclelyTest(desmessages)
    """
    messages = read_datas('/home/wxw/data/httpDatas/http', 'single')
    messages = get_puredatas(messages)
    messages = MessageConvert.filterMsgs([72, 71, 80], messages, 0)
    clsMessages = MessageConvert.clsMessagesByRegix(['GET', 'POST'], 5, messages)
    srcDatas = []
    desDatas = []
    i = 0
    while(i < 252):
        srcDatas.append(clsMessages['GET'][i])
        srcDatas.append(clsMessages['POST'][i])
        i = i + 1
    desDatas.extend(clsMessages['unkown'])
    desDatas = desDatas[0:505]
    message_parser = TextParseLogic()
    srcDatas = message_parser.ConvertDataToMessage(srcDatas, b'\r\n')
    desDatas = message_parser.ConvertDataToMessage(desDatas, b'\r\n')
    #srctextcls = TextClassifyLogicTest(srcDatas, 0.5, 0.4, 0.4, 3)
    #srctextcls.FormatInferCirclelyTest(srcDatas)
    destextcls = TextClassifyLogicTest(desDatas, 0.2, 0.2, 0.2, 3)
    destextcls.FormatInferCirclelyTest(desDatas)
    """
    """
    datas = read_datas('/home/wxw/data/ftp/ftpData', 'multy')
    datasF = []
    for data in datas:
        if len(data) < 100:
            datasF.extend(data)
        else:
            datasF.extend(data[0:500])
    srcDatasF, desDatasF = MessageConvert.clsMessageByDire(datasF)
    srcdatas = get_puredatas(srcDatasF)
    desdatas = get_puredatas(desDatasF)
    message_parser = TextParseLogic()
    srcmessages = message_parser.ConvertDataToMessage(srcdatas, b'\r\n')
    desmessages = message_parser.ConvertDataToMessage(desdatas, b'\r\n')
    srctextcls = TextClassifyLogicTest(srcmessages, 0.2, 0.3, 0.4, 3)
    #srctextcls.FormatInferCirclelyTest(srcmessages)
    destextcls = TextClassifyLogicTest(desmessages, 0.1, 0.1, 0.1, 3)
    #destextcls.getHeadAndNum(desmessages)
    destextcls.FormatInferCirclelyTest(desmessages)
    #destextcls = TextClassifyLogicTest(desmessages, 0.1, 0.1, 0.1, 3)
    #textcls.getHeadAndNum(messages)
    #textcls.FormatInferCirclelyTest(messages)
    """