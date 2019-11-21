from common.readdata import *

class ModBusDataTuning:
    def __init__(self):
        pass

    def getModDatas(self):
        messages = read_datas('/home/wxw/data/modbusdata', 'single')
        messages = get_puredatas(messages)[0:1000]
        return messages

