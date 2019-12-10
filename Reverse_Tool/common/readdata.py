import os
from netzob.all import *
import json



def read_multity_dirs(dirs_list, ways = 'single'):
    t_final_data = []
    if ways == 'single':
        for dir in dirs_list:
            t_final_data.extend(read_datas(dir, 'single'))
    else:
        for dir in dirs_list:
            t_final_data.append(read_datas(dir, 'multisession'))
    return t_final_data

def read_datas(dirs,ways = "single"):
    paths = os.listdir(dirs)
    t_datas = []
    t_sedatas = []
    if ways == "single":
        for path in paths:
            t_path = os.path.join(dirs,path)
            t_data = PCAPImporter.readFile(t_path).values()
            t_datas.extend(t_data)
    else:
        for path in paths:
            t_path = os.path.join(dirs,path)
            t_data = PCAPImporter.readFile(t_path).values()
            t_datas.append(t_data)
    return t_datas

def read_filedatas(filePath):
    print(filePath)
    datas = PCAPImporter.readFile(filePath).values()
    return datas

 
def getSummary(data, lo):
    dataSummary = {}
    dataSummary['id'] = lo
    lo = str(data.date).find('.')
    dataSummary['time'] = '0' + str(data.date)[lo:]
    dataSummary['source'] = data.source
    dataSummary['destination'] = data.destination
    dataSummary['summary'] = 'Len: ' + str(len(data.data))
    return dataSummary

def getSummaries(datas, start):
    i = 0
    resultsSummary = []
    while(i < len(datas)):
        resultsSummary.append(getSummary(datas[i], start + i))
        i = i + 1
    return resultsSummary

def get_puredatas(datas):
    t_fdata = []
    for data in datas:
        t_fdata.append(data.data)
    return t_fdata

def get_data_bylo(datas, start_lo, end_lo=None):
    r_datas = []
    for data in datas:
        if end_lo == None:
            if start_lo < len(data):
                r_datas.append(data[start_lo])
        else:
            if len(data) >= end_lo:
                r_datas.append(data[start_lo:end_lo])
            elif start_lo < len(data):
                r_datas.append(data[start_lo:])
    return r_datas


def get_itoms(string,delimiter):
    return string.split(delimiter)

def add_stail(message,h):
    message_b = bytearray(message)
    for i in range(h):
        message_b.append(250)
    return bytes(message_b)
    
def add_tail(messages,h):
    for i in range(len(messages)):
        messages[i] = add_stail(messages[i],h)
    return messages

def cutmessage(messages,lo_c):
    for i in range(len(messages)):
        messages[i] = messages[i][lo_c:]
    return messages

def get_part(messages, lo):
    t_f = []
    for message in messages:
        t_f.append(message[:lo])
    return t_f

def get_ip(t_str):
    t_lo = t_str.find(':')
    return t_str[0:t_lo]

def clusbydes(messages):
     src = get_ip(messages[0].source)
     des = get_ip(messages[0].destination)
     srcs = []
     dess = []
     for message in messages:
        if(get_ip(message.source) == src):
            srcs.append(message)
        else:
            dess.append(message)
     return srcs,dess

def clusbydesT(Melist):
    src_Me = []
    des_Me = []
    for me in Melist:
        src_t,des_t = clusbydes(me)
        src_Me.extend(src_t)
        des_Me.extend(des_t)
    return src_Me,des_Me

def cut_messages(messages, range):
    cutted_messages = []
    for message in messages:
        if len(message) > range:
            message = message[0:range]
        cutted_messages.append(message)
    return cutted_messages



