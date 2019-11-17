from common.Merger.base_merger import base_merger
from common.FieldTypeInfer.WholeFieldTypeInfer import WholeFieldTypeInfer

class IcsFieldMerger(base_merger):
    def __init__(self, messages):
        super().__init__()
        self.wholeType = WholeFieldTypeInfer(messages)

    def mergeConstFields(self, words, messages):
        wordsType = []
        for word in words:
            if self.wholeType.inferConst(word):
                wordsType.append()