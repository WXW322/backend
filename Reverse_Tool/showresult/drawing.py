import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


fig = plt.figure(num=1, figsize=(10, 5), dpi=80)#开启一个窗口，同时设置大小，分辨率
# ax1 = fig.add_subplot(2, 1, 1)   #通过fig添加子图，参数：行数，列数，第几个。
# ax2 = fig.add_subplot(2, 1, 2)   #通过fig添加子图，参数：行数，列数，第几个。
plt.title("Message Formats Quality Comparison", size=10)
plt.xlabel("Correctness", size=10)
plt.ylabel("Concisness", size=10)
# plt.plot(x, y, "ob")
# plt.plot(x, y, "sr")

plt.axis([0, 105, 0, 105], size=50)                  #设置横纵坐标轴范围，这个在子图中被分解为下面两个函数
# plt.set_xlim(-5,5)                           #设置横轴范围，会覆盖上面的横坐标,plt.xlim
# plt.set_ylim(-10,10)                         #设置纵轴范围，会覆盖上面的纵坐标,plt.ylim



# xmajorLocator = MultipleLocator(20)   #定义横向主刻度标签的刻度差为2的倍数。就是隔几个刻度才显示一个标签文本
# ymajorLocator = MultipleLocator(20)   #定义纵向主刻度标签的刻度差为3的倍数。就是隔几个刻度才显示一个标签文本
# plt.xaxis.set_major_locator(xmajorLocator) #x轴 应用定义的横向主刻度格式。如果不应用将采用默认刻度格式
# plt.yaxis.set_major_locator(ymajorLocator) #y轴 应用定义的纵向主刻度格式。如果不应用将采用默认刻度格式
plt.grid()
plot1 = plt.scatter(68, 95, s=50, marker='o', color='g', label='KFCluster')
plot4 = plt.scatter(100, 100, s=50, marker='o', color='g')
plot2 = plt.scatter(76, 73, s=50, marker='x', color='r', label='LDA+KMEANS')
plot5 = plt.scatter(17, 75, s=50, marker='x', color='r')
plot3 = plt.scatter(64, 76, s=50, marker='^', color='b', label='LDA+DBSCAN')
plot6 = plt.scatter(33, 83, s=50, marker='^', color='b')
# plot2 = plt.plot(30, 35, marker='x', color='r', label='LDA+KMEANS')
# plot3 = plt.plot(2, 80, marker='^', color='b', label='LDA+DBSCAN') #点图：marker图标
# plot2 = plt.plot(x, y, linestyle='--', alpha=0.5, color='r', label='legend2')   #线图：linestyle线性，alpha透明度，color颜色，label图例文本


font1 = {'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 10,
}
plt.legend(loc='upper left', prop=font1)            #显示图例,plt.legend()
# plt.text(100, 100, r'ideal point')                #指定位置显示文字,plt.text()

plt.annotate('FTP', xy=(68, 95), xytext=(69, 96), size=10)
plt.annotate('FTP', xy=(76, 73), xytext=(77, 74), size=10)
plt.annotate('FTP', xy=(64, 76), xytext=(65, 77), size=10)
plt.annotate('HTTP', xy=(100, 100), xytext=(101, 101), size=10)
plt.annotate('HTTP', xy=(17, 75), xytext=(18, 76), size=10)
plt.annotate('HTTP', xy=(33, 83), xytext=(34, 84), size=10)



plt.annotate('ideal point', xy=(100, 100), xytext=(90, 95), size=10,    #添加标注，参数：注释文本、指向点、文字位置、箭头属性
            arrowprops=dict(arrowstyle='->'))


plt.tight_layout()

plt.show()
plt.savefig('drawing1.jpg')













# fig = plt.figure(num=1, figsize=(10, 5), dpi=80)     #开启一个窗口，同时设置大小，分辨率
# plt.title("Message Formats Quality Comparison", size=10)
# plt.xlabel("Correctness", size=10)
# plt.ylabel("Concisness", size=10)
# plt.axis([0, 1.05, 0, 1.05], size=50)                  #设置横纵坐标轴范围，这个在子图中被分解为下面两个函数
# plt.grid()
# plot1 = plt.scatter(.68, .95, s=50, marker='o', color='g', label='KFCluster')
# plot4 = plt.scatter(1.00, 1.00, s=50, marker='o', color='g')
# plot2 = plt.scatter(.76, .73, s=50, marker='x', color='r', label='LDA+KMEANS')
# plot5 = plt.scatter(.17, .75, s=50, marker='x', color='r')
# plot3 = plt.scatter(.64, .76, s=50, marker='^', color='b', label='LDA+DBSCAN')
# plot6 = plt.scatter(.33, .83, s=50, marker='^', color='b')
# font1 = {'family': 'Times New Roman',
#          'weight': 'normal',
#          'size': 10
#          }
# plt.legend(loc='upper left', prop=font1)            #显示图例,plt.legend()
# plt.annotate('FTP', xy=(.68, .95), xytext=(.69, .96), size=10)
# plt.annotate('FTP', xy=(.76, .73), xytext=(.77, .74), size=10)
# plt.annotate('FTP', xy=(.64, .76), xytext=(.65, .77), size=10)
# plt.annotate('HTTP', xy=(1.00, 1.00), xytext=(1.01, 1.01), size=10)
# plt.annotate('HTTP', xy=(.17, .75), xytext=(.18, .76), size=10)
# plt.annotate('HTTP', xy=(.33, .83), xytext=(.34, .84), size=10)
# plt.annotate('ideal point', xy=(1.00, 1.00), xytext=(.90, .95), size=10,
#              arrowprops=dict(arrowstyle='->'))       #添加标注，参数：注释文本、指向点、文字位置、箭头属性
# plt.tight_layout()
# plt.show()
