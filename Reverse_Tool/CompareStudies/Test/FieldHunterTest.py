
from CompareStudies.TextTools.FieldHunter import FieldHunter
from common.readdata import *
from common.DataTuning.RawDataTuning.HttpDataTuning import HttpDataTuning
from common.DataTuning.RawDataTuning.FTPDataTuning import FTPDataTuning
from common.DataTuning.RawDataTuning.RedisDataTuning import RedisDataTuning
from textops.DelimiterFindLogic import *


class FieldHunterTest:
    def __init__(self):
        self.fhunter = FieldHunter()
        self.httpdata = HttpDataTuning()
        self.ftpdata = FTPDataTuning()
        self.redisdata = RedisDataTuning()

    def testFordeliFind(self, dirPath):
        datas = read_datas(dirPath, 'multy')
        datasF = []
        for data in datas:
            if len(data) < 100:
                datasF.extend(data)
            else:
                datasF.extend(data[0:500])
        datas = get_puredatas(datasF)
        print(self.fhunter.findDelimiter(datas))

    def testForHTTPFind(self):
        datas = self.httpdata.sampleDatas()
        print(filterFieldWords(self.fhunter.findDelimiter(datas)))

    def testForFTPFind(self):
        datas = self.ftpdata.sampleData()
        print(filterFieldWords(self.fhunter.findDelimiter(datas)))


    def testForREDISFind(self):
        datas = self.redisdata.sampleDatas()
        print(filterFieldWords(self.fhunter.findDelimiter(datas)))



if __name__ == '__main__':
    fT = FieldHunterTest()
    #fT.testForREDISFind()
    fT.testForFTPFind()
    #fT.testForHTTPFind()
    #fT.testFordeliFind('/home/wxw/data/ftp/ftpData')

