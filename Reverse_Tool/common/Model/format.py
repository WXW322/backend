from netzob.all import *
import six

class format:
    def __init__(self, name = 'symbol'):
        """
        convert a dict datas to a symbol
        sourcedatas: a list of source data
        sourcedata: a tulple, the previous element reprensents the type and the last represents the value 
        """
        self.name = name

    def get_symbols(self, sourcedatas, names):
        """
        convert a dict datas to a symbol
        sourcedatas: a list of source data
        sourcedata: a tulple, the previous element reprensents the type and the last represents the value 
        """
        f_totals = []
        i = 0
        while(i < len(sourcedatas)):
            f_totals.append(self.get_singlesymbol(sourcedatas[i], names[i]))
            i = i + 1
        return f_totals

    def data2f(self, data):
        if data[0] == 'C':
            return Field(name = data[1], domain = data[2])
        elif data[0] == 'L':
            return Field(name = data[1], domain = Alt([element for element in data[2]]))
        else:
            start = data[2][0] * 8
            end = None
            if(data[2][1] != -1):
                end = data[2][1] * 8
            return Field(name = data[1], domain = BitArray(nbBits = (start, end)))
    
    
    def get_singlesymbol(self, sourcedatas, name):
        """
        convert a dict datas to a symbol
        sourcedatas: a list of source data
        sourcedata: a tulple, the previous element reprensents the type and the last represents the value 
        """
        f_totals = []
        for data in sourcedatas:
            f_totals.append(self.data2f(data))
        return Symbol(f_totals, name=name)
            

