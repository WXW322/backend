
from netzob.all import *
import sys


class NetzobTest:
    def __init__(self):
        pass

    def testField(self):
        #tt = Raw('111')
        #print(tt.value.tobytes())
        f0 = Field('hello', name='F0')
        f1 = Field('paris', name='F1')
        f2 = Field('roman', name='F2')
        f0.fields.append(f1)
        f1.fields.append(f2)
        print(f2.getLeafFields(2)[0].name)


if __name__ == '__main__':
    nzTest = NetzobTest()
    nzTest.testField()