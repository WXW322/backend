
from Inferformat.node import node
from showresult.graph_build import tree_graph
import sys


class nodeTest:
    def __init__(self):
        self.Node = node()

    def testGraphBuild(self):
        self.Node.word_type = 'root'
        cone = node(wType= 'F')
        cone.value.append('111')
        ctwo = node(wType='C')
        cone.value.append('222')
        self.Node.children.append(cone)
        self.Node.children.append(ctwo)
        Nodes = []
        Edges = []
        print(' ')
        print(id(ctwo.children))
        print(id(cone.children))
        print(' ')
        self.Node.getGraph(0, Nodes, Edges)
        print(Nodes)
        print(Edges)

    def testGtree(self):
        nodes = [(1, 1), (2, 2), (3, 3), (4, 4)]
        Edges = [(1, 2, 'any'), (2, 3, 'test')]
        tG = tree_graph('a', 'B')
        tG.graph_buildTwo(nodes, Edges)



if __name__ == '__main__':
    gTest = nodeTest()
    gTest.testGtree()
    #gTest.testGraphBuild()