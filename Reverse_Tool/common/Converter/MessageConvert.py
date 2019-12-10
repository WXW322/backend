import scapy.all as scapy
from scapy.utils import PcapReader,PcapWriter
from common.Converter.base_convert import Converter
import sys

class MessageConvert(Converter):
    def __init__(self):
        super(MessageConvert, self).__init__()

    @staticmethod
    def get_ip(t_str):
        t_lo = t_str.find(':')
        return t_str[0:t_lo]

    @staticmethod
    def clsMessageByDire(messages):
        src = MessageConvert.get_ip(messages[0].source)
        des = MessageConvert.get_ip(messages[0].destination)
        srcs = []
        dess = []
        for message in messages:
            if(MessageConvert.get_ip(message.source) == src):
                srcs.append(message)
            else:
                dess.append(message)
        return srcs, dess

    @staticmethod
    def clsMessageIdByDire(messages):
        src = MessageConvert.get_ip(messages[0][1].source)
        des = MessageConvert.get_ip(messages[0][1].destination)
        srcs = []
        dess = []
        for message in messages:
            if (MessageConvert.get_ip(message[1].source) == src):
                srcs.append(message)
            else:
                dess.append(message)
        return srcs, dess

    @staticmethod
    def getMinLength(datas):
        lens = [len(data) for data in datas]
        return min(lens)

    @staticmethod
    def getClsSrcIp(single_pack):
        if 'IP' in single_pack:
            return single_pack['IP'].fields['src']
        else:
            return 'null'

    @staticmethod
    def getClsDesIp(single_pack):
        if 'IP' in single_pack:
            return single_pack['IP'].fields['dst']
        else:
            return 'null'

    @staticmethod
    def clsMessagesByIp(fileFrom, fileTo):
        packages = scapy.rdpcap(fileFrom)
        t_results = {}
        for p in packages:
            srcIp = MessageConvert.getClsSrcIp(p)
            desIp = MessageConvert.getClsDesIp(p)
            if srcIp == 'null' or desIp == 'null':
                continue
            mesKeyFirst = srcIp + desIp
            mesKeySecond = desIp + srcIp
            if mesKeyFirst in t_results:
                t_results[mesKeyFirst].append(p)
            elif (mesKeySecond in t_results):
                t_results[mesKeySecond].append(p)
            else:
                t_results[mesKeyFirst] = []
                t_results[mesKeyFirst].append(p)
        for key in t_results:
            t_temp = t_results[key]
            t_writer = PcapWriter('%s%s.pcap' %(fileTo, key), append=True)
            #t_writer = PcapWriter('/home/wxw/data/cip_datanew/' + key + '.pcap', append=True)
            for p in t_results[key]:
                t_writer.write(p)
            t_writer.flush()
            t_writer.close()

    @staticmethod
    def filterMsgs(valids, messages, lRange=0):
        validMsgs = []
        for message in messages:
            for validItem in valids:
                if str(message[0:lRange]).find(validItem) != -1:
                    validMsgs.append(message)
        return validMsgs

    @staticmethod
    def clsMessagesByRegix(regixS, wLen, messages):
        splitDatas = {}
        for message in messages:
            rightData = str(message[0:wLen])
            lo = False
            for regix in regixS:
                if regix in rightData:
                    if regix not in splitDatas:
                        splitDatas[regix] = []
                    splitDatas[regix].append(message)
                    lo = True
            if not lo:
                if 'unkown' not in splitDatas:
                    splitDatas['unkown'] = []
                splitDatas['unkown'].append(message)
        return splitDatas

    @staticmethod
    def clsMsgsByRegix(regixS, wLen, messages):
        splitDatas = {}
        for message in messages:
            rightData = message[0:wLen]
            for regix in regixS:
                if rightData.find(regix) != -1:
                    if regix not in splitDatas:
                        splitDatas[regix] = []
                    splitDatas[regix].append(message)
                    lo = True
        return splitDatas


if __name__ == '__main__':
    MessageConvert.clsMessagesByIp('/home/wxw/data/http/httpSource/purehttp.pcap', '/home/wxw/data/http/httpSplitOne')
