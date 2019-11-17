import copy

class node:
    def __init__(self, loc = (0, 0), wType = None, ids = None, childs = []):
        self.children = childs
        self.loc = loc
        self.ids = ids
        self.result = []
        self.word_type = wType

    def depth_traverse(self):
        start_node = []
        start_node.append(self)
        self.depth_reverse_node(self, start_node)



    def depth_reverse_node(self, current_node, current_pre):
        if(len(current_node.children) == 0):
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



