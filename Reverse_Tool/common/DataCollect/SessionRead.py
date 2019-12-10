import scapy.all as scapy
from scapy.utils import PcapReader,PcapWriter
import sys
import os
from netzob.all import *

class SessionRead:
    def __init__(self):
        pass

    def cvtDatasToIds(self, datas, lo):
        idDatas = []
        for i in range(len(datas)):
            idData = (i+lo, datas[i])
            idDatas.append(idData)
        return idDatas

    def readIdNetDatas(self, dirs,ways = "single"):
        paths = os.listdir(dirs)
        t_datas = []
        t_id_datas = []
        lo = 0
        if ways == "single":
            for path in paths:
                t_path = os.path.join(dirs, path)
                t_data = PCAPImporter.readFile(t_path).values()
                t_datas.extend(t_data)
        else:
            for path in paths:
                t_path = os.path.join(dirs, path)
                t_data = PCAPImporter.readFile(t_path).values()
                t_datas.append(t_data)
        if ways == 'single':
            t_id_datas = self.cvtDatasToIds(t_datas, 0)
        else:
            lo = 0
            for t_data in t_datas:
                t_id_datas.append(self.cvtDatasToIds(t_data, lo))
                lo = lo + len(t_data)
        return t_id_datas

    def readIdRdDatas(self, dirs,ways = "single"):
        paths = os.listdir(dirs)
        t_datas = []
        t_id_datas = []
        lo = 0
        if ways == "single":
            for path in paths:
                t_path = os.path.join(dirs, path)
                t_data = scapy.rdpcap(t_path)
                t_datas.extend(t_data)
        else:
            for path in paths:
                t_path = os.path.join(dirs, path)
                t_data = scapy.rdpcap(t_path)
                t_datas.append(t_data)
        if ways == 'single':
            t_id_datas = self.cvtDatasToIds(t_datas, 0)
        else:
            lo = 0
            for t_data in t_datas:
                t_id_datas.append(self.cvtDatasToIds(t_data, lo))
                lo = lo + len(t_data)
        return t_id_datas

    def write_Packets(self, filePath, datas):
        t_writer = PcapWriter(filePath, append=True)
        for p in datas:
            t_writer.write(p)
        t_writer.flush()
        t_writer.close()



