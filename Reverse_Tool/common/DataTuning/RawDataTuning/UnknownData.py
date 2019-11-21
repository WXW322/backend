
from common.readdata import *


class UnkownData:
    def __init__(self):
        pass

    def DataTuning(self):
        messages = read_datas('/home/wxw/data/Netzobum', 'multy')
        for message in messages:
            print(len(message))
            print('aaa')
            for data in message:
                print(data)


if __name__ == '__main__':
    uuData = UnkownData()
    uuData.DataTuning()