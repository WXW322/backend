
from common.Converter.base_convert import Converter


class ConverterTest:
    def __init__(self):
        self.cvt = Converter()

    def filterBsTest(self, boundaries, rge):
        print(self.cvt.filterB(boundaries, rge))


if __name__ == '__main__':
    cvtTest = ConverterTest()
    cvtTest.filterBsTest([(0, 1), (1, 4), (4, 6), (6, 8), (8, 9)], 7)