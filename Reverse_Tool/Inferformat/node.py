import copy
from common.FieldTypeInfer.LocalFieldTypeInfer import LocalFieldTypeInfer
from common.Converter.base_convert import Converter

class node:
    def __init__(self, loc = (0, 0), ids = None, wType = None, childs = []):
        self.children = childs
        self.loc = loc
        self.ids = ids
        self.result = []
        self.word_type = wType
        self.value = []
        self.localF = LocalFieldTypeInfer()


    def depth_traverse(self):
        start_node = []
        start_node.append(self)
        self.depth_reverse_node(self, start_node)


    def depth_reverse_node(self, current_node, current_pre):
        print(id(current_node), len(current_node.children))
        if(len(current_node.children) == 0):
            print('sss')
            self.result.append(current_pre)
        else:
            for child_node in current_node.children:
                next_pre = copy.deepcopy(current_pre)
                next_pre.append(child_node)
                self.depth_reverse_node(child_node, next_pre)

    def print_tree(self, way):
        if(way == "single"):
            for stem in self.result:
                print("format_start")
                for leaf in stem:
                    print(leaf.loc)
        else:
            pass

    def get_prefix(self, loc_e):
        pass


    def getNodeData(self):
        nodeDatas = []
        if self.ids != None:
            for data in self.ids:
                nodeDatas.append(data.getData(self.loc))
        return nodeDatas

    def getNodeType(self):
        datas = self.getNodeData()
        Lens = []
        for data in self.ids:
            Lens.append(len(data.message))
        if self.localF.inferConst(datas):
            self.word_type = 'C'
        elif self.loc[1] - self.loc[0] <= 4 and self.localF.inferLen(datas, Lens):
            self.word_type = 'L'
        elif self.localF.inferFunc(datas):
            self.word_type = 'F'
        else:
            self.word_type = 'V'

    def upDataByType(self):
        datas = self.getNodeData()
        if self.word_type == 'C':
            self.value.append(datas[0])
        elif self.word_type == 'F':
            dicDatas = Converter().convert_raw_to_count(datas)
            for key in dicDatas:
                self.value.append(key)

    def splitNode(self):
        cnodes = []
        tchilddatas = {}
        for data in self.ids:
            item = data.getData(self.loc)
            if item not in tchilddatas:
                tchilddatas[item] = []
            tchilddatas[item].append(data)
        for key in tchilddatas:
            tcnode = node(self.loc, tchilddatas[key], self.word_type)
            tcnode.upDataByType()
            if self.loc[0] == 0:
                print(tcnode.word_type, tcnode.value)
            cnodes.append(tcnode)
        return cnodes

    def showTree(self, h):
        stList = [' ' for i in range(h)]
        prestr = ''.join(stList)
        print(prestr + str(self.loc) + str(self.word_type) + str(self.value))
        for child in self.children:
            child.showTree(h+1)




