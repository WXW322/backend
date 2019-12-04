
from Config.ftp import ftp
import sys


class FTPParser:
    def __init__(self):
        self.ttfp = ftp()

    def parseMsg(self, message):
        strMsg = str(message)
        boundaries = []
        index = 0
        boundaries.append(0)
        while(strMsg.find(' ', index) != -1):
            lo = strMsg.find(' ', index)
            boundaries.append(lo-2)
            index = lo + 1
        index = 0
        while(strMsg.find('\r\n', index) != -1):
            lo  = strMsg.find('\r\n')
            boundaries.append(lo-2)
            index = index + 1
        boundaries.append(len(message))
        return boundaries

    def parseMsgs(self, msgs):
        FBoundaries = []
        for msg in msgs:
            FBoundaries.append(self.parseMsg(msg))
        return FBoundaries



