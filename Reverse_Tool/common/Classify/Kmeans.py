
from sklearn.cluster import KMeans
import numpy as np

class KmeansClasser:
    def __init__(self):
        pass

    def clsDatas(self, datas, K):
        kmeans_model = KMeans(n_clusters = K, random_state=1).fit(datas)
        return kmeans_model

    def clsMessages(self, messages, datas, K):
        kMeansResult = self.clsDatas(datas, K)
        dataLabels = kMeansResult.labels_
        i = 0
        clsMessages = {}
        while(i < len(dataLabels)):
            key = dataLabels[i]
            if key not in clsMessages:
                clsMessages[key] = []
            clsMessages[key].append(messages[i])
            i = i + 1
        return clsMessages


if __name__ == '__main__':
    datas = np.array([[1, 2, 1], [2, 1, 3], [3, 3, 3], [4, 1, 3]])
    kmcls = KmeansClasser()
    kmcls.clsDatas(datas)

