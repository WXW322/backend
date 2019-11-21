
from sklearn.cluster import DBSCAN
from common.Classify.BaseClasser import BaseClasser
import numpy as np

class DbScanClasser(BaseClasser):
    def __init__(self):
        pass

    def clsDatas(self, datas, eps, minPt):
        clser = DBSCAN(eps=eps, min_samples=minPt)
        labelResults =clser.fit(datas)
        return labelResults

    def clsMessages(self, messages, datas, eps, minPt):
        clsLabels = self.clsDatas(datas, eps, minPt)
        return self.clsMsgs(clsLabels, messages)

    def caculateEura(self, listA, listB):
        return np.linalg.norm(np.array(listA) - np.array(listB))

    def caculateEuras(self, lists):
        dis = [[0 for j in range(len(lists[0]))] for i in range(len(lists))]
        for i in range(len(lists)):
            for j in range(len(lists[0])):
                if i != j:
                    dis[i][j] = self.caculateEura(lists[i], lists[j])
        return dis

