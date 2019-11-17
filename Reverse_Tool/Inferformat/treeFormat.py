from Inferformat.treef import *
from Inferformat.node import *
from common.Model.PrimData import primeData

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
                t_v.append(t_num[key])
        if len(t_v) > 0:
            t_node = node((t_start, -1), t_v)
            t_r.append(t_node)
        return t_r
