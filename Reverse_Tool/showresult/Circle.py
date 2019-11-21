# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt


class CircleDraw:
    def __init__(self):
        pass

    def draw(self):
        plt.rcParams.update({'font.size': 13})
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        plt.figure(figsize=(6, 6))  # 将画布设定为正方形，则绘制的饼图是正圆
        label = ['GET', 'POST', 'HTTP 200 OK', 'others']  # 定义饼图的标签，标签是列表
        explode = [0.01, 0.01, 0.01, 0.01]  # 设定各项距离圆心n个半径
        # plt.pie(values[-1,3:6],explode=explode,labels=label,autopct='%1.1f%%')#绘制饼图
        values = [4142, 665, 4516, 105]
        plt.pie(values, explode=explode, labels=label, autopct='%1.1f%%')  # 绘制饼图
        plt.title(u'HTTP Distribution', fontproperties="SimHei")  # 绘制标题
        plt.savefig('/home/wxw/paper/researchresult/text/statics/httpdis.png')  # 保存图片
        plt.show()