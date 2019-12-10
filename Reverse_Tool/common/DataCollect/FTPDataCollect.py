from common.readdata import *
from common.Converter.MessageConvert import MessageConvert
from textops.TextParseLogic import TextParseLogic
from common.DataCollect.SessionRead import SessionRead

class FTPDataCollect:
    def __init__(self):
        self.msgP = TextParseLogic()
        self.cmds = {b'PWD', b'331 Please specify the password', b'RETR', b'TYPE I', b'250 Directory successfully changed',
                     b'227 Entering Passive Mode', b'PASS', b'150 Ok to send data',
                     b'226 Directory send OK', b'220', b'226 Transfer complete', b'230 Login successful',
                     b'NLST', b'STOR', b'LIST', b'USER',
                     b'550 Create directory operation', b'200 Switching to', b'150 Opening BINARY mode data connection for',
                     b'150 Here comes the directory listing', b'200 Switching to ASCII mode', b'MKD', b'257', b'TYPE A',
                     b'CWD', b'PASV'}
        self.seRead = SessionRead()


    def getDatas(self):
        datas = read_datas('/home/wxw/data/ftp/ftpData', 'single')
        datas = get_puredatas(datas)
        return datas

    def getDiff(self, datas):
        desDatas = self.msgP.ConvertDataToMessage(datas, b'\r\n')
        desNowDatas = [datanow.now() for datanow in desDatas]
        diff = {}
        for desNow in desNowDatas:
            # desNow = str(desNow).split(' ')[0]
            desNow = str(desNow)
            lo = desNow.find('(')
            if lo != -1:
                desNow = desNow[0:lo]
            lo = desNow.find('/')
            if lo != -1:
                desNow = desNow[0:lo]
            if desNow not in diff:
                diff[desNow] = 1
            else:
                diff[desNow] = diff[desNow] + 1
        print(diff)

    def tuningTwoHttpBydire(self):
        srcData, desData = self.tuningHttpByregix()
        message_parser = TextParseLogic()
        desDatas = message_parser.ConvertDataToMessage(srcData, b'\r\n')
        desNowDatas = [datanow.now() for datanow in desDatas]
        diff = {}
        for desNow in desNowDatas:
            #desNow = str(desNow).split(' ')[0]
            desNow = str(desNow)
            lo = desNow.find('(')
            if lo != -1:
                desNow = desNow[0:lo]
            lo = desNow.find('/')
            if lo != -1:
                desNow = desNow[0:lo]
            if desNow not in diff:
                diff[desNow] = 1
            else:
                diff[desNow] = diff[desNow] + 1
        print(diff)

    def tuningHttpBydire(self):
        messages = read_datas('/home/wxw/data/httpDatas/http', 'single')
        messages = get_puredatas(messages)
        messages = MessageConvert.filterMsgs(['GET', 'POST', 'HTTP'], messages, 10)
        clsMessages = MessageConvert.clsMessagesByRegix(['GET', 'POST'], 5, messages)
        clsDesMessages = clsMessages['unkown']
        message_parser = TextParseLogic()
        desDatas = message_parser.ConvertDataToMessage(clsDesMessages, b'\r\n')
        desNowDatas = [datanow.now() for datanow in desDatas]
        diff = {}
        for desNow in desNowDatas:
            if desNow not in diff:
                diff[desNow] = 1
            else:
                diff[desNow] = diff[desNow] + 1
        print(diff)


    def tuningHttpByregix(self):
        datas = read_datas('/home/wxw/data/ftp/ftpData', 'multy')
        datasF = []
        for data in datas:
            if len(data) < 100:
                datasF.extend(data)
            else:
                datasF.extend(data[0:500])
        srcDatasF, desDatasF = MessageConvert.clsMessageByDire(datasF)
        srcDatasF = get_puredatas(srcDatasF)
        desDatasF = get_puredatas(desDatasF)
        print(len(desDatasF))
        return srcDatasF, desDatasF

    def tuningHttpIdByregix(self):
        datas = self.seRead.readIdRdDatas('/home/wxw/data/ftp/ftpData', 'multy')
        datasF = []
        for data in datas:
            if len(data) < 100:
                datasF.extend(data)
            else:
                datasF.extend(data[0:500])
        filePath = '/home/wxw/data/DataTest/FTP/192.168.2.2Ftp.pcap'
        self.seRead.write_Packets(filePath, datasF)



    def getTotalData(self):
        Tdatas = []
        srcD, desD = self.tuningHttpByregix()
        Tdatas.extend(srcD)
        Tdatas.extend(desD)
        return Tdatas

    def sampleData(self):
        datas = self.getDatas()
        datasSplit = MessageConvert.clsMsgsByRegix(self.cmds, 20, datas)
        Fdatas = []
        for key in datasSplit:
            print(key, len(datasSplit[key]))
            if len(datasSplit[key]) > 1000:
                print('zzz')
                Fdatas.extend(datasSplit[key][0:500])
            else:
                Fdatas.extend(datasSplit[key])
        print(len(Fdatas))
        return Fdatas

    def getTotalCommond(self):
        datas = self.getDatas()
        self.getDiff(datas)

if __name__ == '__main__':
    ftpCollect = FTPDataCollect()
    ftpCollect.tuningHttpIdByregix()
