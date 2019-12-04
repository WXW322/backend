
from common.Converter.base_convert import Converter

def TestMergeDicts():
    dicOne = {'a': 111, 'b': 22, 'c': 10}
    dicTwo = {'a': 11, 'd': 22, 'c': 10}
    dicThree = {'a': 111, 'e': 22, 'f': 10}
    L = [dicOne, dicTwo, dicThree]
    print(Converter().MergeListDics(L))

def TestHex():
    ss = b'123456'
    hexSS = ''
    for x in ss:
        hexSS = hexSS + hex(x) + ' '
    print(hexSS)

def TestHexConvert():
    cvt = Converter()
    print(cvt.MergeListGroup([[1, 3, 4]], [[2, 5, 6]]))

if __name__ == '__main__':
    TestHexConvert()