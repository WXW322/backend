from abc import *

class treef(object):
    __class__ = ABCMeta

    def __init__(self, datas):
        self.datas = datas
        self.tree = None
    @abstractmethod
    def generate_T(self):
        pass




