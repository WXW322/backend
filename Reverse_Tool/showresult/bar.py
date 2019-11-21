import numpy as np
import matplotlib.pyplot as plt
import os
import sys

def draw_pic(a,b,path):
    plt.rcParams.update({'font.size': 14})
    plt.ylim((0.0,1.10))
    total_width, n = 0.6, 2
    width = total_width / n
    x = np.array([1,3,5])
    x = x - (total_width - width) / 2
    names = ['modbus','iec104','Ethernet/ip']
    plt.bar(x, a, width=width, label='IPRFW',facecolor = '#009E73')
    plt.bar(x + width, b, width=width, label='FieldH',facecolor = '#9400D3')
    plt.xticks(x + width / 2, names)
    plt.legend(bbox_to_anchor = (0.54,0.9))
    fpath = os.path.join(path,'tid.jpg')
    plt.savefig(fpath)
    plt.close('all')
    
def draw_pict(a,b,path):
    plt.rcParams.update({'font.size': 16})
    plt.ylim((0.0,1.10))
    total_width, n = 0.3, 2
    width = total_width / n
    x = np.array([1,3])
    x = x - (total_width - width) / 2
    names = ['modbus','iec104']
    plt.bar(x, a, width=width, label='IPRFW',facecolor = '#009E73')
    plt.bar(x + width, b, width=width, label='FieldH',facecolor = '#9400D3')
    plt.xticks(x + width / 2, names)
    plt.legend(bbox_to_anchor = (0.35, 0.94))
    fpath = os.path.join(path,'tid.jpg')
    plt.savefig(fpath)
    plt.close('all')

    #plt.xticks(x + width/2,names)
a = np.array([1.0, 1.0])
b = np.array([1.0, 1.0])
draw_pict(a, b, '/home/wxw/paper/researchresult/icccn/words')
sys.exit()
a = np.array([1.0,1.0,1.0])
b = np.array([1.0,1.0,1.0])
draw_pic(a,b,'/home/wxw/paper/researchresult/icccn/words')
sys.exit()
#b = np.array([0.6667,0.3333,0.2222])
#a = np.array([0.7241,0.3333,0.2414])
#draw_pic(a,b,'/home/wxw/paper/researchresult/classify/iec104/pic')
a = np.array([0.5,0.5,0.25])
b = np.array([1.0,1.0,1.0])
draw_pic(a,b,'/home/wxw/paper/researchresult/classify/cip/pic')
