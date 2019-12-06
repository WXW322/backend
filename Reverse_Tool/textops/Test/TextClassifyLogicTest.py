
from textops.TextClassifyLogic import TextClassifyLogic
from common.readdata import *
from textops.TextParseLogic import TextParseLogic
from common.Converter.MessageConvert import MessageConvert
from common.DataTuning.RawDataTuning.HttpDataTuning import HttpDataTuning
from common.DataTuning.RawDataTuning.FTPDataTuning import FTPDataTuning
from common.DataTuning.RawDataTuning.RedisDataTuning import RedisDataTuning
from textops.TextSympolToTree import TextSympolToTree
from showresult.graph_build import tree_graph
from Inferformat.node import node
import sys

class TextClassifyLogicTest:
    def __init__(self, messages, srate, rrate, trate, h):
        self.textcls = TextClassifyLogic(messages, srate, rrate, trate, h)
        self.txtSymTree = TextSympolToTree()
        self.Tgraph = tree_graph('a', 'B')

    def FormatInferCirclelyTest(self, messages):
        fFormats = self.textcls.FormatInferCirclely(messages)
        for f in fFormats:
            nodeT = self.txtSymTree.symbolToTree(f)
            nodeT.showTree(0)
            #print(len(f.fields))
            #print(f._str_debug())

    def FormatInferCirclelyTestTwo(self, messages, tPath, wTtpe):
        fFormats = self.textcls.FormatInferCirclely(messages, wTtpe)
        nodeRoot = node(wType='root')
        for f in fFormats:
            nodeT = self.txtSymTree.subSymbolToTree(f)
            nodeRoot.children.append(nodeT)
        nodeRoot.showTree(0)
        self.Tgraph.graph_buildFour(nodeRoot, tPath)
        #self.Tgraph.graph_buildFour(nodeRoot, '/home/wxw/paper/researchresult/text/formatInfer/KFCluster 0.05 0.2 0.2 3 httpsp.png')



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

    def ftpTestOne(self, DirPath):
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

    def httpTest(self, DirPath=''):
        httptuning = HttpDataTuning()
        datas = httptuning.sampleDatas()
        message_parser = TextParseLogic()
        datas = message_parser.ConvertDataToMessage(datas, b'\r\n')
        #srctextcls = TextClassifyLogicTest(datas, 0.05, 0.2, 0.2, 3)
        #srctextcls = TextClassifyLogicTest(datas, 0.02, 0.2, 0.2, 3)
        srctextcls = TextClassifyLogicTest(datas, 0.02, 0.1, 0.1, 3)
        srctextcls.FormatInferCirclelyTest(datas)

    def httpGenerateTest(self):
        httptuning = HttpDataTuning()
        datas = httptuning.sampleDatas()
        message_parser = TextParseLogic()
        datas = message_parser.ConvertDataToMessage(datas, b'\r\n')
        srctextcls = TextClassifyLogicTest(datas, 0.05, 0.2, 0.2, 3)
        # srctextcls = TextClassifyLogicTest(datas, 0.02, 0.2, 0.2, 3)
        # srctextcls = TextClassifyLogicTest(datas, 0.02, 0.1, 0.1, 3)
        srctextcls.FormatInferCirclelyTestTwo(datas, '/home/wxw/paper/researchresult/text/formatInfer/KFCluster/httpOne.png', 'H')

    def ftpTest(self):
        ftptuning = FTPDataTuning()
        datas = ftptuning.sampleData()
        message_parser = TextParseLogic()
        datas = message_parser.ConvertDataToMessage(datas, b'\r\n')
        #srctextcls = TextClassifyLogicTest(datas, 0.1, 0.3, 0.3, 3)
        srctextcls = TextClassifyLogicTest(datas, 0.1, 0.2, 0.2, 3)
        srctextcls.FormatInferCirclelyTest(datas)

    def ftpGenerateTest(self):
        ftptuning = FTPDataTuning()
        datas = ftptuning.sampleData()
        message_parser = TextParseLogic()
        datas = message_parser.ConvertDataToMessage(datas, b'\r\n')
        # srctextcls = TextClassifyLogicTest(datas, 0.1, 0.3, 0.3, 3)
        srctextcls = TextClassifyLogicTest(datas, 0.1, 0.2, 0.2, 3)
        srctextcls.FormatInferCirclelyTestTwo(datas)


    def redisTest(self):
        redisDataTuning = RedisDataTuning('/home/wxw/data/RedisData')
        #srcDatas, desDatas = redisDataTuning.getProDatas()
        #samplesrcmsgs = redisDataTuning.sampleSourceDatas(srcDatas, 2)
        #print(samplesrcmsgs[0])
        srcDatas = redisDataTuning.sampleDatas()
        message_parser = TextParseLogic()
        srcmessages = message_parser.ConvertDataToMessage(srcDatas, b'\r\n', h=2)
        #desmessages = message_parser.ConvertDataToMessage(desDatas, b'\r\n', h=1)
        srctextcls = TextClassifyLogicTest(srcmessages, 0.05, 0.2, 0.2, 3)
        srctextcls.FormatInferCirclelyTest(srcmessages)
        #destextcls = TextClassifyLogicTest(desmessages, 0.3, 0.3, 0.3, 2)
        #destextcls.FormatInferCirclelyTest(desmessages)

    def redisGenerateTest(self):
        redisDataTuning = RedisDataTuning('/home/wxw/data/RedisData')
        # srcDatas, desDatas = redisDataTuning.getProDatas()
        # samplesrcmsgs = redisDataTuning.sampleSourceDatas(srcDatas, 2)
        # print(samplesrcmsgs[0])
        srcDatas = redisDataTuning.sampleDatas()
        message_parser = TextParseLogic()
        srcmessages = message_parser.ConvertDataToMessage(srcDatas, b'\r\n', h=2)
        # desmessages = message_parser.ConvertDataToMessage(desDatas, b'\r\n', h=1)
        srctextcls = TextClassifyLogicTest(srcmessages, 0.05, 0.2, 0.2, 3)
        srctextcls.FormatInferCirclelyTestTwo(srcmessages, '/home/wxw/paper/researchresult/text/formatInfer/KFCluster/redisshortOne', 'R')




if __name__ == '__main__':
    message_parser = TextClassifyLogicTest([], 0.1, 0.1, 0.1, 0.1)
    #message_parser.redisGenerateTest()
    message_parser.httpGenerateTest()
    #message_parser.ftpGenerateTest()
    #message_parser.ftpTest()
    #message_parser.httpTest()
    #message_parser.redisTest()
    #httptuning = HttpDataTuning()
    #srcDatas, desDatas = httptuning.tuningHttpByregix()
    """
    ftpTuning = FTPDataTuning()
    srcDatas, desDatas = ftpTuning.tuningHttpByregix()
    desmessages = message_parser.ConvertDataToMessage(desDatas, b'\r\n')
    destextcls = TextClassifyLogicTest(desmessages, 0.05, 0.2, 0.2, 3, 2)
    destextcls.FormatInferCirclelyTest(desmessages)
    """
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