
import os
from Data_base.Data_mysql.MysqlDeal import MysqlDeal
from common.Converter.TimeCvter import TimeCvter

class FileWriteLogic:
    def __init__(self):
        self.path = '/home/wxw/data/userUpload'
        self.mysql = MysqlDeal()
        self.tmCvt = TimeCvter()

    def getFileLen(self, fileName):
        fileName = os.path.join(self.path, fileName)
        fSize = os.path.getsize(fileName)
        return fSize

    def writeMySql(self, fileName):
        try:
            fileSize = self.getFileLen(fileName)
            nowDay = self.tmCvt.getNowTimeStr()
            fileDatas = {'name': fileName, 'size': str(fileSize), 'timeNow': nowDay}
            self.mysql.insertFile(fileDatas)
        except Exception:
            print(Exception)

    def readMySqlSize(self):
        results = self.mysql.select()
        fSize = 0
        for result in results:
            nSize = int(result[2])
            fSize = fSize + nSize
        fSize = int(fSize/1000)
        return str(fSize) + 'k'

    def readFileLists(self):
        pass


if __name__ == '__main__':
    fileWriter = FileWriteLogic()
    print(fileWriter.readMySqlSize())
    #fileWriter.writeMySql('141.81.0.10141.81.0.24.pcap')
