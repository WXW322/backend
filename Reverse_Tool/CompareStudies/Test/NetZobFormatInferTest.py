

from CompareStudies.BinaryProtocols.FormatInfer import NetZobFormatInfer
from common.DataTuning.RawDataTuning.ModBusDataTuning import ModBusDataTuning


class NetZobFormatInferTest:
    def __init__(self):
        self.nz = NetZobFormatInfer()
        self.md = ModBusDataTuning()

    def clsModbus(self):
        datas = self.md.getModDatas()
        self.nz.clsMessages(datas)

    def clsFTP(self):
        pass


if __name__ == '__main__':
    nzFormatTest = NetZobFormatInferTest()
    nzFormatTest.clsModbus()