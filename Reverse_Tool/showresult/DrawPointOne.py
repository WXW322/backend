import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

fig = plt.figure(num=1, figsize=(10, 5), dpi=80)     #开启一个窗口，同时设置大小，分辨率
plt.title("Message Formats Quality Comparison", size=10)
plt.xlabel("Correctness", size=10)
plt.ylabel("Concisness", size=10)
plt.axis([0, 1.05, 0, 1.05], size=50)                  #设置横纵坐标轴范围，这个在子图中被分解为下面两个函数
plt.grid()
plot1 = plt.scatter(.8750, .5769, s=50, marker='o', color='g', label='KFCluster')
plot4 = plt.scatter(.8000, .7000, s=50, marker='o', color='g')
plot7 = plt.scatter(.8182, .8182, s=50, marker='o', color='g')
plot2 = plt.scatter(.5333, .5385, s=50, marker='x', color='r', label='LDA+KMEANS')
plot5 = plt.scatter(.9000, .8000, s=50, marker='x', color='r')
plot8 = plt.scatter(.8000, .8182, s=50, marker='x', color='r')
plot3 = plt.scatter(.3333, .5769, s=50, marker='^', color='b', label='LDA+DBSCAN')
plot6 = plt.scatter(.8000, .9000, s=50, marker='^', color='b')
plot9 = plt.scatter(.2500, .8182, s=50, marker='^', color='b')
font1 = {'family': 'Times New Roman',
          'weight': 'normal',
          'size': 10
          }
plt.legend(loc='upper left', prop=font1)            #显示图例,plt.legend()
plt.annotate('FTP', xy=(.8750, .5769), xytext=(.8570, .5869), size=10)
plt.annotate('FTP', xy=(.5333, .5385), xytext=(.5333, .5485), size=10)
plt.annotate('FTP', xy=(.3333, .5769), xytext=(.3333, .5869), size=10)
plt.annotate('HTTP', xy=(.8000, .7000), xytext=(.8000, .7100), size=10)
plt.annotate('HTTP', xy=(.9000, .8000), xytext=(.9000, .8100), size=10)
plt.annotate('HTTP', xy=(.8000, .9000), xytext=(.8000, .9100), size=10)
plt.annotate('REDIS', xy=(.8182, .8182), xytext=(.8182, .7782), size=10)
plt.annotate('REDIS', xy=(.8000, .8182), xytext=(.7700, .8282), size=10)
plt.annotate('REDIS', xy=(.2500, .8182), xytext=(.2500, .8282), size=10)
plt.annotate('ideal point', xy=(1.00, 1.00), xytext=(.90, .95), size=10,
              arrowprops=dict(arrowstyle='->'))       #添加标注，参数：注释文本、指向点、文字位置、箭头属性
plt.tight_layout()
plt.savefig('/home/wxw/paper/researchresult/text/classify/cls.jpg')
