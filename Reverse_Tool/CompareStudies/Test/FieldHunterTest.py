
from CompareStudies.TextTools.FieldHunter import FieldHunter
from common.readdata import *


class FieldHunterTest:
    def __init__(self):
        self.fhunter = FieldHunter()

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



if __name__ == '__main__':
    fT = FieldHunterTest()
    fT.testFordeliFind('/home/wxw/data/ftp/ftpData')

