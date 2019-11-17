from netzob.all import *
import common.Model.format
import StateM.Stateline
import common.readdata

def test_normal():
    f1 = Field(name = "f1", domain = "111")
    f2 = Field(name = "f2", domain = ASCII(nbChars=(2, 3)))
    f3 = Field(name = "f3", domain = "like")
    f = Symbol([f1, f2, f3])
    aa, bb = AbstractField.abstract("2111ablike", [f])
    print(type(aa) == UnknownSymbol)

def test_int():
    f1 = Field(name = "f1", domain = 10)
    f2 = Field(name = "f2", domain = '111')
    f3 = Field(name = "f3", domain = "like")
    f = Symbol([f1, f2, f3])
    aa, bb = AbstractField.abstract("2111ablike", [f])
    print(type(aa) == UnknownSymbol)
 

def test_bytes():
    f1 = Field(name = 'f1', domain = b'x')
    tt = BitArray(nbBits = (16, 24))
    f2 = Field(name = 'f2', domain = tt)
    f3 = Field(name = 'f3', domain = b'cc')
    f = Symbol([f1, f2, f3])
    aa, bb = AbstractField.abstract(b'xaacc', [f])
    print(bb)
   
def test_f():
    s_datas = [[('C', 'function', 'GET'), ('V', 'payload', (0, -1))], [('C', 'funciton', 'POST'), ('V', 'payload', (0, -1))],\
               [('C', 'function', b'HTTP/1.1'), ('V', 'payload', (0, -1))]]
    f = format.format("http")
    symbols = f.get_symbols(s_datas)
    return symbols

def testState(path):
    t_datas = readdata.read_datas(path)[0:20]
    t_datas = readdata.get_puredatas(t_datas)
    symbols = test_f()
    State = Stateline.StateLine(symbols)
    Results = State.messages2sym(t_datas)
    for result in Results:
        print(result)
    
    
testState('/home/wxw/data/http')


