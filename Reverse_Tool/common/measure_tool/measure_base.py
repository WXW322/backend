from abc import *

class Base_measure:
    __class__ = ABCMeta

    def __init__(self):
        pass
    @abstractmethod
    def Measure(self, DataTure, DataPredict):
        pass

