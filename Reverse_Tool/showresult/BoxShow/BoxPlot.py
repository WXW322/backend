
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

def plotBox(dict):
    labels = []
    datas = []
    for key in dict:
        labels.append(key)
        datas.append(dict[key])
    plt.boxplot(datas, labels=labels)
    plt.show()
    #plt.savefig('/home/wxw/paper/researchresult/BinaryFormat/BorderTest/box.png')

if __name__ == '__main__':
    dictas = {'a' :[0.5, 0.1, 0.4], 'b':[0.2, 0.4, 0.6]}
    plotBox(dictas)