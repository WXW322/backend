from Inferformat.treef import *
from Inferformat.node import *
from common.Model.PrimData import primeData
import queue
import sys

class treeFormat(treef):
    def __init__(self, datas, T_c, T_r):
        super(treeFormat, self).__init__(datas)
        self.R = T_r
        self.C = T_c

    def generate_T(self):
        t_ids = []
        self.tree = node()
        self.tree.children = self.generate_node(self.datas)
        return self.tree

    def generateNT(self):
        t_ids = []
        self.tree = node()
        self.tree.word_type = 'root'
        self.tree.children = self.generateNode(self.datas, self.tree, 0, 10)
        return self.tree

    def generateSplitNT(self):
        t_ids = []
        self.tree = node()
        self.tree.word_type = 'root'
        self.tree.children = self.generateSplitNode(self.datas, self.tree, 0, 7)
        return self.tree

    def generate_node(self, datas):
        t_r = []
        t_start = datas[0].now()
        t_num = {}
        for data in datas:
            t_next = data.nextLoc()
            if t_next not in t_num:
                t_num[t_next] = []
            t_num[t_next].append(data)
        t_v = []
        for key in t_num:
            if float(len(t_num[key])) / float(len(datas)) >= self.R and len(t_num[key]) >= self.C:
                t_node = node((t_start, key), t_num[key])
                if t_start != key:
                    t_node.children = t_node.children + self.generate_node(t_num[key])
                t_r.append(t_node)
            else:
                t_v.extend(t_num[key])
        if len(t_v) > 0:
            t_node = node((t_start, -1), t_v)
            t_r.append(t_node)
        return t_r

    def generateNode(self, datas, prenode, depth, maxD):
        t_r = []
        t_start = datas[0].now()
        if depth >= maxD:
            tNode = node((t_start, -1), datas)
            tNode.word_type = 'Continue'
            return [tNode]
        t_num = {}
        for data in datas:
            t_next = data.nextLoc()
            if t_next not in t_num:
                t_num[t_next] = []
            t_num[t_next].append(data)
        t_v = []
        for key in t_num:
            if key < 0:
                print(t_num[key][0].relaloc, t_num[key][0].boundaries)
            if float(len(t_num[key])) / float(len(datas)) >= self.R and len(t_num[key]) >= self.C:
                t_node = node((t_start, key), t_num[key])
                t_node.getNodeType()
                t_node.upDataByType()
                if t_start != key:
                    t_node.children = t_node.children + self.generateNode(t_num[key], t_node, depth + 1, maxD)
                    #t_node.children = t_node.children + self.generate_node(t_num[key])
                t_r.append(t_node)
            else:
                t_v.extend(t_num[key])
        if len(t_v) > 0:
            if len(t_v) < self.C:
                t_node = node((t_start, -1), t_v)
                t_node.word_type = 'VL'
                t_r.append(t_node)
            else:
                maxData = max([m.now() for m in t_v])
                print(maxData, t_start)
                if maxData > t_start:
                    for pridata in t_v:
                        pridata.updateLo()
                    if prenode.word_type != 'LV':
                        t_node = node((t_start, maxData), t_v)
                        t_node.word_type = 'LV'
                        t_node.children = t_node.children + self.generateNode(t_v, t_node, depth + 1, maxD + 1)
                        t_r.append(t_node)
                    else:
                        t_r.extend(self.generateNode(t_v, prenode, depth + 1, maxD))
                else:
                    t_node = node((t_start, -1), t_v)
                    t_node.word_type = 'LV'
                    t_r.append(t_node)
        return t_r

    def generateSplitNode(self, datas, prenode, depth, maxD):
        t_r = []
        t_start = datas[0].now()
        if depth >= maxD:
            tNode = node((t_start, -1), datas)
            tNode.word_type = 'Continue'
            return [tNode]
        t_num = {}
        for data in datas:
            t_next = data.nextLoc()
            if t_next not in t_num:
                t_num[t_next] = []
            t_num[t_next].append(data)
        t_v = []
        for key in t_num:
            if float(len(t_num[key])) / float(len(datas)) >= self.R and len(t_num[key]) >= self.C:
                t_node = node((t_start, key), t_num[key])
                t_node.getNodeType()
                t_node.upDataByType()
                if t_start != key:
                    if t_node.word_type != 'F':
                        t_node.children = t_node.children + self.generateSplitNode(t_num[key], t_node, depth + 1, maxD)
                        t_r.append(t_node)
                    else:
                        childNodes = t_node.splitNode()
                        for childnode in childNodes:
                            childnode.children = childnode.children + self.generateSplitNode(childnode.ids, childnode, depth + 1, maxD)
                            t_r.append(childnode)
                    # t_node.children = t_node.children + self.generate_node(t_num[key])
            else:
                t_v.extend(t_num[key])
        if len(t_v) > 0:
            if len(t_v) < self.C:
                t_node = node((t_start, -1), t_v)
                t_node.word_type = 'LV'
                t_r.append(t_node)
            else:
                maxData = max([m.now() for m in t_v])
                print(maxData, t_start)
                if maxData > t_start:
                    for pridata in t_v:
                        pridata.updateLo()
                    if prenode.word_type != 'LV':
                        t_node = node((t_start, maxData), t_v)
                        t_node.word_type = 'LV'
                        t_node.children = t_node.children + self.generateSplitNode(t_v, t_node, depth + 1, maxD + 1)
                        t_r.append(t_node)
                    else:
                        t_r.extend(self.generateSplitNode(t_v, prenode, depth + 1, maxD))
                else:
                    t_node = node((t_start, -1), t_v)
                    t_node.word_type = 'LV'
                    t_r.append(t_node)
        return t_r


    def layyerTree(self):
        firstQueue = queue.Queue()
        secondqueue = queue.Queue()
        firstQueue.put(self.tree)
        lo = 0
        while(not firstQueue.empty() or not secondqueue.empty()):
            print('ccc')
            if lo == 0:
                while(not firstQueue.empty()):
                    tN = firstQueue.get()
                    print(tN.loc, tN.word_type, tN.value)
                    for child in tN.children:
                        secondqueue.put(child)
                lo = 1
            else:
                while (not secondqueue.empty()):
                    tN = secondqueue.get()
                    print(tN.loc, tN.word_type, tN.value)
                    for child in tN.children:
                        firstQueue.put(child)
                lo = 0

