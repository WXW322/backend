
from common.Classify.Kmeans import KmeansClasser
import numpy as np

class KmeansClasserTest:
    def __init__(self):
        self.kmeansCls = KmeansClasser()

    def MsgsClsTest(self, datas, messages, K):
        print(self.kmeansCls.clsMessages(messages, datas, K))


if __name__ == '__main__':
    kmsTest = KmeansClasserTest()
    datas = np.array([[1, 2, 1], [2, 1, 3], [3, 3, 3], [4, 1, 3]])
    msgs = ['aa', 'bb', 'bb', 'bb', 'bb']
    print(kmsTest.MsgsClsTest(datas, msgs, 2))