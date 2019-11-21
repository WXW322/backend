import numpy as np
from common.Classify.Dbscan import DbScanClasser

class DbscanTest:
    def __init__(self):
        self.dbscan = DbScanClasser()

    def clsDataTest(self):
        X = np.array([[1, 2], [2, 2], [2, 3], [8, 7], [8, 8], [25, 80]])
        print(self.dbscan.clsDatas(X, 3, 2).labels_)

    def testDisCacu(self):
        x = [[1, 1, 0], [2, 3, 1], [1, 2, 1]]
        print(self.dbscan.caculateEuras(x))


if __name__ == '__main__':
    dbscanTest = DbscanTest()
    dbscanTest.testDisCacu()
    #dbscanTest.clsDataTest()