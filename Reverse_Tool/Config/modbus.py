from common.readdata import *
from common.ranker import *
from common.Converter.word_converter import word_convert


class modbus:
    def __init__(self):
        self.coms = []
        self.lo = 7
        self.fields = [(0, 2), (2, 5), (5, 6), (6, 7), (7, 8), (8, 10), (10, 12), (8, 9), (12, 13)]

    def GetMessageBorder(self, message):
        return word_convert().itemtoborder(self.fields)

