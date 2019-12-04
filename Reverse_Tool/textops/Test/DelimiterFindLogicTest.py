
from textops.DelimiterFindLogic import *
from common.readdata import *
from common.DataTuning.RawDataTuning.HttpDataTuning import HttpDataTuning
from common.DataTuning.RawDataTuning.FTPDataTuning import FTPDataTuning
from common.DataTuning.RawDataTuning.RedisDataTuning import RedisDataTuning

def testForDeliFind(dirPath):
    datas = read_datas(dirPath, 'multy')
    datasF = []
    for data in datas:
        if len(data) < 100:
            datasF.extend(data)
        else:
            datasF.extend(data[0:500])
    datas = get_puredatas(datasF)
    freWords, deliword = getDelimiter(datas)
    print(freWords, deliword)

def getHTTPdelimiter():
    httpDatas = HttpDataTuning()
    datas = httpDatas.sampleDatas()
    freWords, deliword = getDelimiter(datas)
    print(freWords, deliword)

def getFTPdelimiter():
    ftpDatas = FTPDataTuning()
    datas = ftpDatas.sampleData()
    freWords, deliword = getDelimiter(datas)
    print(freWords, deliword)

def getRidisData():
    redisDatas = RedisDataTuning()
    datas = redisDatas.sampleDatas()
    freWords, deliword = getDelimiter(datas)
    print(freWords, deliword)

if __name__ == '__main__':
    getRidisData()
    #getFTPdelimiter()
    #getHTTPdelimiter()
    #testForDeliFind('/home/wxw/data/ftp/ftpData')