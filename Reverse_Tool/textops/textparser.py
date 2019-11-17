"""
This class is mainly for split text messages.
Give it message data and delimiter, it will
return the split results. 
"""

import sys
from netzob.all import *
from common.readdata import *
import time
import functools

class textparser:
    def __init__(self):
        self.name = 'parser'

    def split(self, messages, delimiter):
        t_messages = []
        for message in messages:
            t_messages.append(RawMessage(data=message))
        symbol = Symbol(messages=t_messages)
        Format.splitDelimiter(symbol, ASCII(delimiter))
        result = symbol.getCells()
        print(len(result))
        return result

    def teststates(self):
        pass

def compare_now(s1, s2):
    if s1[0] < s2[0]:
        return 1
    elif s1[0] > s2[0]:
        return -1
    else:
        if s1[1] > s2[1]:
            return 1
        elif s1[1] < s2[1]:
            return -1
        else:
            return 0

def addNum(L, time):
    if time != 0:
        addNum(L, time-1)
    L.append(time)


if __name__ == '__main__':
    L = []
    addNum(L, 10)
    print(L)


