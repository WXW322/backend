
from common.Parser.FTPParser import FTPParser
from common.DataTuning.RawDataTuning.FTPDataTuning import FTPDataTuning


class TestFTP:
    def __init__(self):
        self.ff = FTPParser()
        self.ftpData = FTPDataTuning()

    def parseMsgs(self):
        ftpDatas = FTPDataTuning().getTotalData()
        return self.ff.parseMsgs(ftpDatas)


if __name__ == '__main__':
    testf = TestFTP()
    print(testf.parseMsgs())
