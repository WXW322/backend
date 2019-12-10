
from textops.TextViewLogic import TextViewLogic


class TextViewLogicTest:
    def __init__(self):
        self.textView = TextViewLogic()

    def spltMsgs(self):
        print(self.textView.spltMsgs())

    def testFrrmatTree(self):
        print(self.textView.formatInfer())

if __name__ == '__main__':
    txtTest = TextViewLogicTest()
    txtTest.testFrrmatTree()
    #txtTest.spltMsgs()