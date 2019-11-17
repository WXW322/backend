from common.FieldTypeInfer.WholeFieldTypeInfer import WholeFieldTypeInfer
from common.readdata import *

class TestWholeField:
    def __init__(self, messages, locs):
        self.messages = messages
        self.locs = locs
        self.gFieldInfer = WholeFieldTypeInfer()

    def TestConst(self, lo):
        lodatas = []
        for message in self.messages:
            if len(message) > lo[-1]:
                lodatas.append(message[lo[0]:lo[1]])
        return self.gFieldInfer.inferConst(lodatas)


if __name__ == '__main__':
    messages = read_datas('/home/wxw/data/ToolDatas/15895903730.10.222', 'single')
    messages = get_puredatas(messages)
    testWholeField = TestWholeField(messages, [(0, 1), (3, 5)])
    print(testWholeField.TestConst((2, 5)))
