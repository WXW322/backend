import numpy as np
import matplotlib.pyplot as plt
import os
import sys

class FigureGenerator:
    def __init__(self):
        self.barWidth = 0.15

    def plotBar(self, xLables, dataYOne, dataYTwo, xLabel, yLabel, ylimData):
        x = [2, 3, 4]
        font = {'font.size': 18}
        plt.rcParams.update(font)
        plt.rcParams['figure.dpi'] = 300
        rectsOne = plt.bar(left=x, height=dataYOne, width=self.barWidth, label=xLabel, facecolor = '#009E73')
        rectsTwo = plt.bar(left=[i + self.barWidth for i in x], height=dataYTwo, width=self.barWidth, label=yLabel, facecolor='#9400D3')
        plt.ylim(ylimData)
        #plt.xticks([index + self.barWidth for index in x], xLables)
        plt.xticks([index + self.barWidth/2 for index in x], xLables)
        #plt.legend(bbox_to_anchor = (0.53,0.62), frameon = False)
        plt.legend(frameon = False)
        #plt.savefig('/home/wxw/research_result/modbus/two.png')
        #plt.savefig('/home/wxw/research_result/iec104/two.png')
        plt.savefig('/home/wxw/research_result/cip/two.png')
        #plt.show()

    def plotLine(self, dataX, dataY, xLabel, yLabel, xlim, ylim, colors, labels, markers, xRanges, yRanges):
        plt.rcParams.update({'font.size': 18})
        plt.rcParams['figure.dpi'] = 300
        #plt.tight_layout()
        plt.gcf().subplots_adjust(bottom=0.15)
        plt.xlabel(xLabel)
        plt.ylabel(yLabel)
        plt.xlim(xlim)
        plt.ylim(ylim)
        i = 0
        while(i < len(dataX)):
            plt.plot(dataX[i], dataY[i], colors[i], label = labels[i], marker = markers[i])
            i = i + 1
        plt.xticks(xRanges[0], xRanges[1])
        plt.yticks(yRanges[0], yRanges[1])
        plt.legend(loc=2)
        #plt.legend(loc=3)
        #plt.show()
        plt.savefig('/home/wxw/research_result/cip/f1/three.png')



if __name__ == '__main__':
    barGenerator = FigureGenerator()
    """
    #generate figure
    datas_X = [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]]
    datas_f1mod = [[0, 0.5000, 0.2500, 0.2857], [0, 0.4444, 0.4444, 0.4444], [0, 0.6000, 0.9231, 0.9231]]
    datas_Yf1iec = [[0, 0.5714, 0.5714, 0.6667], [0, 0.6667, 0.4, 0.5333], [0, 0.8696, 0.9090, 0.7368]]
    datas_Yf1cip = [[0, 0.3077, 0.1538, 0.3750], [0, 0.5, 0.5, 0.40], [0, 0.4, 0.6667, 0.6667]]
    ylim = (0, 1.45)
    xlim = (1, 4.2)
    xranges = ([1,2,3,4],['1','2','3','4'])
    yranges = ([0.0,0.2,0.4,0.6,0.8,1.0],[0.0,0.2,0.4,0.6,0.8,1.0])
    xlabel = 'tree-depth'
    ylabel = 'F1-Measure'
    colors = ['r', 'b', '#1EFF1E']
    labels = ['LDA', 'VE', 'RGVE']
    markers = ["o", "+", "s"]
    barGenerator.plotLine(datas_X, datas_Yf1cip, xlabel, ylabel, xlim, ylim, colors, labels, markers, xranges, yranges)
    """
    """
    generate length fig
    datas_X = [[a for a in np.arange(0.1, 1.1, step=0.1)] for _ in range(3)]
    datas_Y = [[1.0 for _ in range(10)], [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.5], [1.0 for _ in range(10)]]
    ylim = (0.1, 1.3)
    xlim = (0.1, 1.03)
    xranges = ([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0'])
    yranges = ([0.0, 0.2, 0.4, 0.6, 0.8, 1.0], [0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    xlabel = 'T_R'
    ylabel = 'Ratio'
    colors = ['r', 'b', '#1EFF1E']
    labels = ['modbus', 'iec104', 'ethernet/cip']
    markers = ["o", "+", "s"]
    barGenerator.plotLine(datas_X, datas_Y, xlabel, ylabel, xlim, ylim, colors, labels, markers, xranges, yranges)
    """

    #generate bar figure
    xLabels = ['correct', 'precision', 'combine']
    datamodbusYOne = [0.8, 0.75, 0.6]
    datamodbusYTwo = [1.0, 1.0, 1.0]
    dataiec104YTwo = [0.6667, 0.3333, 0.2222]
    dataiec104YOne = [0.7241, 0.3333, 0.2414]
    datacipYOne = [0.5, 0.5, 0.25]
    datacipYTwo = [1.0, 1.0, 1.0]
    xLabel = 'netzob'
    yLabel = 'IPART'
    #ylimData = (0.0, 1.10)
    #ylimData = (0.0, 1.10)
    ylimData = (0.0, 1.40)
    #barGenerator.plotFigure(xLabels, datamodbusYOne, datamodbusYTwo, xLabel, yLabel, ylimData)
    #barGenerator.plotFigure(xLabels, dataiec104YOne, dataiec104YTwo, xLabel, yLabel, ylimData)
    barGenerator.plotBar(xLabels, datacipYOne, datacipYTwo, xLabel, yLabel, ylimData)
