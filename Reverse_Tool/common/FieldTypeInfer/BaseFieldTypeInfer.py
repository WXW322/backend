
from abc import ABCMeta, abstractmethod

class BaseFieldTypeInfer(metaclass=ABCMeta):
    @abstractmethod
    def inferConst(self, datas):
        pass

    @abstractmethod
    def inferSeriesId(self, datas):
        pass

    @abstractmethod
    def inferFunc(self, datas):
        pass

    @abstractmethod
    def inferLen(self, datas):
        pass
    
