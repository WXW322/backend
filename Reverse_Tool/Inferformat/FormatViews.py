from Inferformat.treef import treef
from Inferformat.treeFormat import treeFormat
from common.Model.PrimData import primeData

def getFormat(datas, tR, tC):
    formatTree = treeFormat(datas, tC, tR)
    formatTree.generate_T()
    return formatTree.tree

def convertTreeToList(tree):
    tree.depth_traverse()
    tree.print_tree('single')

if __name__ == '__main__':
    t_temp = []
    t_temp.append(primeData('11122',[0, 1, 3, 5, 7]))
    t_temp.append(primeData('11222',[0, 1, 3, 5, 9]))
    t_temp.append(primeData('112234',[0, 1, 3, 5, 10]))
    t_temp.append(primeData('123423',[0, 2, 4, 6, 7]))
    t_temp.append(primeData('1121',[0, 2, 4, 6, 8]))
    t_temp.append(primeData('123123',[0, 2, 4, 6, 10]))
    tree_builder = treeFormat(t_temp, 3, 0.2)
    t_result = tree_builder.generate_T()
    t_result.depth_traverse()
    for f in t_result.result:
        print("format start")
        for node_i in f:
            print(node_i.loc)