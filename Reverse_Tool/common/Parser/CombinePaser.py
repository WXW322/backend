from Config.modbus import modbus
from common.Parser.FTPParser import FTPParser


class ComPaser:
    def __init__(self):
        self.ftpP = FTPParser()
        self.modP = modbus()

    def parseMsg(self, message):
        strMsg = str(message)
        if strMsg.find('\\r\\n') != -1:
            #print(str(strMsg))
            #print(self.ftpP.parseMsg(message))
            return self.ftpP.parseMsg(message)
        else:
            #print(str(message))
            #print(self.modP.GetMessageBorder(message))
            return self.modP.GetMessageBorder(message)

    def parseMsgs(self, messages):
        return [self.parseMsg(message) for message in messages]
