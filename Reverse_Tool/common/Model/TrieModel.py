

class TrieModel:
    def __init__(self):
        self.children = {}
        self.cnt = 1

    def insertNode(self, value):
        if value[0] in self.children:
            self.children[value[0]] = self.children[value[0]] + 1
        else:
            self.children[value[0]] = TrieModel()
        if len(value) > 1:
            self.children[value[0]].insertNode(value[1:])

    def queryNode(self, value):
        if len(value) == 1:
            return self.children

