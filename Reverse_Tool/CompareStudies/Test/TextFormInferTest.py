
from CompareStudies.TextTools.TextFormInfer import TextFormInfer
from common.readdata import *
from common.Converter.MessageConvert import MessageConvert
from common.DataTuning.RawDataTuning.HttpDataTuning import HttpDataTuning
from common.DataTuning.RawDataTuning.FTPDataTuning import FTPDataTuning
from common.DataTuning.RawDataTuning.RedisDataTuning import RedisDataTuning
import sys
from textops.TextSympolToTree import TextSympolToTree

class TextFormInferTest:
    def __init__(self, messages):
        self.tFomInfer = TextFormInfer(messages)
        self.httpdata = HttpDataTuning()
        self.ftpData = FTPDataTuning()
        self.redisData = RedisDataTuning()
        self.txtSymTree = TextSympolToTree()

    def ldaFormatInferTest(self, wSize, TK, wLen, Kcls, path = '', infercls='H'):
        fNums = self.tFomInfer.ldaFormatInfer(wSize, TK, wLen, Kcls, infercls)
        self.txtSymTree.symbolsToTree(fNums, path)
        #for fnum in fNums:
        #    nodeT = self.txtSymTree.symbolToTree(fnum)
        #    nodeT.showTree(0)
            #print(fnum._str_debug())



    def ladDbscanFormatInfer(self, wSize, TK, wLen, mindis, minpt, path = '', infercls='H'):
        fNums = self.tFomInfer.ladDbscanFormatInfer(wSize, TK, wLen, mindis, minpt, infercls)
        self.txtSymTree.symbolsToTree(fNums, path)
        #for fnum in fNums:
         #   print(fnum._str_debug())

    def httpDataTest(self):
        srcDatas, desDatas = self.httpdata.tuningHttpByregix()
        self.tFomInfer = TextFormInfer(desDatas)
        self.ldaFormatInferTest(3, 15, 2, 4)

    def httpTotalTest(self):
        datas = self.httpdata.sampleDatas()
        self.tFomInfer = TextFormInfer(datas)
        self.ldaFormatInferTest(3, 15, 2, 5)


    def httpTotalDBSTest(self):
        datas = self.httpdata.sampleDatas()
        self.tFomInfer = TextFormInfer(datas)
        self.ladDbscanFormatInfer(3, 5, 3, 0.15, 10)

    def ftpTotalTest(self):
        datas = self.ftpData.sampleData()
        self.tFomInfer = TextFormInfer(datas)
        #self.ldaFormatInferTest(3, 15, 2, 10)
        self.ladDbscanFormatInfer(3, 5, 3, 0.05, 10)
        #self.ldaFormatInferTest(3, 15, 2, 15)
        #self.ldaFormatInferTest(3, 15, 2, 20)
        #self.ldaFormatInferTest(3, 15, 2, 10)
        #self.ldaFormatInferTest(3, 15, 2, 5)

    def ftpTotalGenerate(self):
        datas = self.ftpData.sampleData()
        self.tFomInfer = TextFormInfer(datas)
        #self.ldaFormatInferTest(3, 15, 2, 15, '/home/wxw/paper/researchresult/text/formatInfer/KMEANS/15 ftp one.png')
        #self.ladDbscanFormatInfer(3, 15, 3, 0.01, 4, '/home/wxw/paper/researchresult/text/formatInfer/DBSCAN/0.01 ftp.png')
        self.ladDbscanFormatInfer(3, 15, 3, 0.05, 10,'/home/wxw/paper/researchresult/text/formatInfer/DBSCAN/0.05 ftp.png')
        self.ladDbscanFormatInfer(3, 5, 3, 0.05, 10)




    def httpDataTestDBS(self):
        httpDataTuning = HttpDataTuning()
        srcMsgs, desMsgs = httpDataTuning.tuningHttpByregix()
        self.tFomInfer = TextFormInfer(desMsgs)
        self.ladDbscanFormatInfer(3, 5, 3, 0.15, 10)

    def ftpDataTest(self):
        srcDatas, desDatas = self.ftpData.tuningHttpByregix()
        self.tFomInfer = TextFormInfer(srcDatas)
        self.ldaFormatInferTest(3, 15, 3, 15)

    def ftpDataTestDBS(self):
        httpDataTuning = FTPDataTuning()
        srcMsgs, desMsgs = httpDataTuning.tuningHttpByregix()
        print(len(srcMsgs) + len(desMsgs))
        self.tFomInfer = TextFormInfer(desMsgs)
        self.ladDbscanFormatInfer(3, 15, 3, 0.01, 4)

    def redisTotalTest(self):
        datas = self.redisData.sampleDatas()
        self.tFomInfer = TextFormInfer(datas)
        #self.ladDbscanFormatInfer(3, 5, 3, 0.10, 10)
        #self.ladDbscanFormatInfer(3, 5, 3, 0.10, 20)
        #self.ladDbscanFormatInfer(3, 5, 3, 0.01, 20)
        #self.ladDbscanFormatInfer(3, 5, 3, 0.2, 20)
        #self.ldaFormatInferTest(3, 15, 2, 5)
        self.ldaFormatInferTest(3, 15, 2, 10)
        #self.ldaFormatInferTest(3, 15, 2, 15)
        #self.ldaFormatInferTest(3, 15, 2, 20)

    def redisTotalGenerate(self):
        datas = self.redisData.sampleDatas()
        self.tFomInfer = TextFormInfer(datas)
        self.ladDbscanFormatInfer(3, 5, 3, 0.05, 4, '/home/wxw/paper/researchresult/text/formatInfer/DBSCAN/redis .png')
        #self.ldaFormatInferTest(3, 15, 2, 10, '/home/wxw/paper/researchresult/text/formatInfer/KMEANS/11 three redis.png')

    def httpTotalGenerate(self, kClus):
        datas = self.httpdata.sampleDatas()
        self.tFomInfer = TextFormInfer(datas)
        print('ss', kClus)
        #self.ladDbscanFormatInfer(3, 5, 3, 0.05, 10, '/home/wxw/paper/researchresult/text/formatInfer/DBSCAN/0.15 http.png')
        self.ldaFormatInferTest(3, 15, 2, kClus, '/home/wxw/paper/researchresult/text/formatInfer/KMEANS/'
                                + str(kClus) + 'httptwo.png', infercls='H')
        print('ee', kClus)

    def httpTotalRepeatGenerate(self, kClus, rTime):
        datas = self.httpdata.sampleDatas()
        self.tFomInfer = TextFormInfer(datas)
        self.ldaFormatInferTest(3, 15, 2, kClus, '/home/wxw/paper/researchresult/text/formatInfer/KMEANS/'
                                    + str(kClus) + ' ' + str(rTime) + 'httpone.png', infercls='H')

    def httpDBSTotalGenerate(self, r, C, rTime=''):
        datas = self.httpdata.sampleDatas()
        self.tFomInfer = TextFormInfer(datas)
        print('ss', r)
        self.ladDbscanFormatInfer(3, 5, 3, r, C,
                                  '/home/wxw/paper/researchresult/text/formatInfer/DBSCAN/'
                                  + str(r) + str(C) + rTime +'httptwo.png', infercls='H')
        #self.ldaFormatInferTest(3, 15, 2, kClus, '/home/wxw/paper/researchresult/text/formatInfer/KMEANS/'
                                #+ str(kClus) + 'httpone.png', infercls='H')
        print('ee', r)

    def ftpTotalGenerate(self, kClus):
        datas = self.ftpData.sampleData()
        self.tFomInfer = TextFormInfer(datas)
        self.ldaFormatInferTest(3, 15, 2, kClus, '/home/wxw/paper/researchresult/text/formatInfer/KMEANS/FTP/'
                                + str(kClus) +'ftp.png', infercls='F')
        #self.ladDbscanFormatInfer(3, 15, 3, 0.01, 4, '/home/wxw/paper/researchresult/text/formatInfer/DBSCAN/0.01 ftp.png')
        #self.ladDbscanFormatInfer(3, 15, 3, 0.05, 10,
        #                          '/home/wxw/paper/researchresult/text/formatInfer/DBSCAN/0.05 ftp.png')
        #self.ladDbscanFormatInfer(3, 5, 3, 0.05, 10)

    def ftpTotalGenerateRepeat(self, kClus, rTime):
        datas = self.ftpData.sampleData()
        self.tFomInfer = TextFormInfer(datas)
        self.ldaFormatInferTest(3, 15, 2, kClus, '/home/wxw/paper/researchresult/text/formatInfer/KMEANS/FTP/'
                                + str(kClus) + str(rTime) +'ftp.png', infercls='F')
        #self.ladDbscanFormatInfer(3, 15, 3, 0.01, 4, '/home/wxw/paper/researchresult/text/formatInfer/DBSCAN/0.01 ftp.png')
        #self.ladDbscanFormatInfer(3, 15, 3, 0.05, 10,
        #                          '/home/wxw/paper/researchresult/text/formatInfer/DBSCAN/0.05 ftp.png')
        #self.ladDbscanFormatInfer(3, 5, 3, 0.05, 10)

    def ftpDBSCANGenerate(self, r, C, rTime=''):
        datas = self.ftpData.sampleData()
        self.tFomInfer = TextFormInfer(datas)
        print('ss', r)
        self.ladDbscanFormatInfer(3, 5, 3, r, C,
                                  '/home/wxw/paper/researchresult/text/formatInfer/DBSCAN/FTP/'
                                  + str(r) + str(C) + rTime + 'ftp.png', infercls='F')
        # self.ldaFormatInferTest(3, 15, 2, kClus, '/home/wxw/paper/researchresult/text/formatInfer/KMEANS/'
        # + str(kClus) + 'httpone.png', infercls='H')
        print('ee', r)

    def redisTotalGenerate(self, kClus, rTime=''):
        datas = self.redisData.sampleDatas()
        self.tFomInfer = TextFormInfer(datas)
        self.ldaFormatInferTest(3, 15, 2, kClus, '/home/wxw/paper/researchresult/text/formatInfer/KMEANS/REDIS/'
                                + str(kClus) + rTime + 'redis.png', infercls='R')
        #self.ladDbscanFormatInfer(3, 5, 3, 0.05, kClus, '/home/wxw/paper/researchresult/text/formatInfer/DBSCAN/redis .png')

    def redisDBSCANGenerate(self, r, C, rTime=''):
        datas = self.redisData.sampleDatas()
        self.tFomInfer = TextFormInfer(datas)
        print('ss', r)
        self.ladDbscanFormatInfer(3, 5, 3, r, C,
                                  '/home/wxw/paper/researchresult/text/formatInfer/DBSCAN/REDIS/'
                                  + str(r) + str(C) + rTime + 'redis.png', infercls='R')
        # self.ldaFormatInferTest(3, 15, 2, kClus, '/home/wxw/paper/researchresult/text/formatInfer/KMEANS/'
        # + str(kClus) + 'httpone.png', infercls='H')
        print('ee', r)

if __name__ == '__main__':
    textFTest = TextFormInferTest(['aaa'])
    #textFTest.httpTotalRepeatGenerate(10, 4)
    #textFTest.redisDBSCANGenerate(0.01, 10, str(4))
    #textFTest.ftpDBSCANGenerate(0.05, 10, str(4))
    #textFTest.httpDBSTotalGenerate(0.01, 10, str(3))
    for i in [0.01, 0.05, 0.1, 0.2]:
        textFTest.httpDBSTotalGenerate(i, 10)
    #    textFTest.redisDBSCANGenerate(i, 10)
    #    textFTest.ftpDBSCANGenerate(i, 10)
    #    textFTest.httpDBSTotalGenerate(i, 10)
    #for c in [5, 10, 15, 20]:
    #    textFTest.redisDBSCANGenerate(0.01, c)
    #    textFTest.ftpDBSCANGenerate(0.01, c)
    #    textFTest.httpDBSTotalGenerate(0.01, c)
    #textFTest.httpTotalRepeatGenerate(10, 1)
    #textFTest.redisTotalGenerate(10, str(4))
    #textFTest.ftpTotalGenerate(10, 4)
        #textFTest.httpTotalRepeatGenerate(10, i)
    #textFTest.httpTotalGenerate(20)
    #for i in [5, 10, 15, 20]:
    #    textFTest.httpTotalGenerate(i)
    #    textFTest.redisTotalGenerate(i)
    #    textFTest.ftpTotalGenerate(i)

    #textFTest.redisTotalGenerate()
    #textFTest.ftpTotalGenerate()
    #textFTest.httpTotalGenerate()
    #textFTest.redisTotalTest()
    #textFTest.ftpTotalTest()
    #textFTest.httpTotalTest()
    #textFTest.httpTotalDBSTest()
    #textFTest.ftpDataTestDBS()
    #textFTest.ftpDataTest()
    #textFTest.httpDataTestDBS()
    #textFTest.httpDataTest()
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
    srctextFormattest = TextFormInferTest(srcdatas)
    #srctextFormattest.ldaFormatInferTest(3, 8, 3, 5)
    destextFormattest = TextFormInferTest(desdatas)
    #destextFormattest.ldaFormatInferTest(3, 3, 3, 5)
    #destextFormattest.ldaFormatInferTest(3, 3, 3, 5)
    """
    """
    messages = read_datas('/home/wxw/data/httpDatas/http_measure', 'single')
    messages = get_puredatas(messages)
    textFormattest = TextFormInferTest(messages)
    textFormattest.ldaFormatInferTest(3, 8, 3, 5)
    """
