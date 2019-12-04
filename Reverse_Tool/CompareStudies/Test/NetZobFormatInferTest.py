

from CompareStudies.BinaryProtocols.FormatInfer import NetZobFormatInfer
from common.DataTuning.RawDataTuning.ModBusDataTuning import ModBusDataTuning
from common.DataTuning.RawDataTuning.FTPDataTuning import FTPDataTuning
import sys


class NetZobFormatInferTest:
    def __init__(self):
        self.nz = NetZobFormatInfer()
        self.md = ModBusDataTuning()
        self.ftpdata = FTPDataTuning()

    def clsModbus(self):
        datas = self.md.getModDatas()
        dic = set()
        for data in datas:
            item = data[7:8]
            dic.add(item)
        print(len(dic))
        sys.exit()
        self.nz.clsMessages(datas)

    def clsFTP(self):
        datas = self.ftpdata.getTotalData()
        self.nz.clsMessages(datas)

    def clsMix(self):
        Tdatas = []
        Tdatas.extend(self.md.getModDatas())
        Tdatas.extend(self.ftpdata.getTotalData())
        self.nz.clsMessages(Tdatas, 60)


if __name__ == '__main__':
    nzFormatTest = NetZobFormatInferTest()
    nzFormatTest.clsModbus()
    #nzFormatTest.clsFTP()
    #nzFormatTest.clsFTP()
    #nzFormatTest.clsModbus()