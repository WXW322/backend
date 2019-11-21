
from textops.DelimiterFindLogic import *
from common.readdata import *

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



if __name__ == '__main__':
    testForDeliFind('/home/wxw/data/ftp/ftpData')