
from common.readdata import *
from common.DataTuning.RawDataTuning.FTPDataTuning import FTPDataTuning
import sys


class DataTuning:
    def __init__(self):
        self.ftp = FTPDataTuning()

    def readDatas(self, filePath):
        datas= read_filedatas(filePath)
        datas = get_puredatas(datas)
        return datas

    def readDatasTemp(self, filePath):
        srcDatas, desDatas = self.ftp.tuningHttpByregix()
        datas = []
        datas.extend(srcDatas)
        datas.extend(desDatas)
        return datas