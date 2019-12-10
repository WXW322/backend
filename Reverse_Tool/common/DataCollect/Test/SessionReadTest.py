
from common.DataCollect.SessionRead import SessionRead

class SessionReadTest:
    def __init__(self):
        self.sessionR = SessionRead()

    def IdReadTest(self):
        datas = self.sessionR.readIdNetDatas('/home/wxw/data/ftp/ftpData', 'multy')
        datasOne = self.sessionR.readIdRdDatas('/home/wxw/data/ftp/ftpData', 'multy')
        for i in range(len(datas)):
            print(datas[i][0][0], datas[i][0][1].source)
            print(datasOne[i][0])




if __name__ == '__main__':
    sessionReadTest = SessionReadTest()
    sessionReadTest.IdReadTest()