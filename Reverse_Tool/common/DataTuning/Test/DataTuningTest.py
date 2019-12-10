
from common.DataTuning.RawDataTuning.DataTuning import DataTuning

class DataTuningTest:
    def __init__(self):
        self.dataTuning = DataTuning()

    def readDatasByTypeTest(self, fileType):
        datas = self.dataTuning.readDatasByType(fileType)
        print(datas[0])


if __name__ == '__main__':
    dataTuningTest = DataTuningTest()
    dataTuningTest.readDatasByTypeTest('textPro')