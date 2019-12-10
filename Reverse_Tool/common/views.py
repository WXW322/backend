from django.shortcuts import render
import json
from django.http.response import HttpResponse
from .GlobalModels.PrimModel import PrimeModel
from .readdata import *
from .Converter.base_convert import Converter
from IcsProtocol.Logic.GVoterLogic import GvoterLogic
from Config.UserConfig import UserConfig
from IcsProtocol.Config.GveConf import GveConf
from common.DataTuning.RawDataTuning.DataTuning import DataTuning
from BinaryProtocol.Logic.MsgSplitLogic import MegSplitLogic
from IcsProtocol.Logic.FormatGeneLogic import FormatGeneLogic
from textops.TextViewLogic import TextViewLogic
from IcsProtocol.Logic.IcsReverLogic import IcsReverLogic
# Create your views here.

def getDatas(request):
    datas = request.POST.items()
    keys = []
    for data in datas:
        keys.append(data[0])
    sendDatas = json.loads(keys[0])
    pageOrder = sendDatas.get('pageNum')
    pageCnt = sendDatas.get('pageCnt')
    proType = sendDatas.get('proType')
    dataTuning = DataTuning()
    startNum = int(pageOrder) * int(pageCnt)
    #messageDatas = read_datas('/home/wxw/data/ToolDatas/15895903730.10.222', 'single')
    messageDatas = dataTuning.readSummaryByType(proType)
    PrimeModel.messages = messageDatas
    messageSummaries = []
    if startNum < len(PrimeModel.messages):
        if startNum + pageCnt < len(PrimeModel.messages):
            messageSummaries = getSummaries(PrimeModel.messages[startNum:startNum+pageCnt], startNum)
        else:
            messageSummaries = getSummaries(PrimeModel.messages[startNum:], startNum)
    else:
        pass
    return HttpResponse(json.dumps(messageSummaries), content_type= 'application/json')

def getProtoDataDetail(request):
    datas = request.POST.items()
    keys = []
    for data in datas:
        keys.append(data[0])
    sendDatas = json.loads(keys[0])
    rowIndex = sendDatas.get('rowIndex')
    proType = sendDatas.get('proType')
    dataTuning = DataTuning()
    reHexData = None
    print(proType)
    if proType == 'icsPro':
        messageDatas = dataTuning.readDatasByType(proType)
        msgData = messageDatas[rowIndex]
        hexData = Converter().byteListToHex(msgData)
        reHexData = {'res': hexData}
    elif proType == 'textPro':
        messageDatas = dataTuning.readDatasByType(proType)
        msgData = messageDatas[rowIndex]
        hexData = str(msgData)
        reHexData = {'res': hexData}
    else:
        messageDatas = dataTuning.readDatasByType(proType)
        msgData = messageDatas[rowIndex]
        hexData = Converter().byteListToHex(msgData)
        reHexData = {'res': hexData}
    return HttpResponse(json.dumps(reHexData), content_type= 'application/json')

def getPostJson(request):
    datas = request.POST.items()
    keys = []
    for data in datas:
        keys.append(data[0])
    sendDatas = json.loads(keys[0])
    return sendDatas

def convertResponseDatas(messages, startLo):
    t_results = []
    j = 0
    for message in messages:
        tData = {}
        tData['id'] = startLo + j
        tData['data'] = message
        t_results.append(tData)
        j = j + 1
    return t_results


def getProtoSplitSummary(request):
    postDatas = getPostJson(request)
    pageOrder = postDatas.get('pageNum')
    pageCnt = postDatas.get('pageCnt')
    proType = postDatas.get('proType')
    print(proType)
    startNum = int(pageOrder) * int(pageCnt)
    dataTuning = DataTuning()
    # future
    #messageDatas = dataTuning.readDatas('/home/wxw/data/ToolDatas/15895903730.10.222')
    #messageDatas = read_datas('/home/wxw/data/ToolDatas/15895903730.10.222', 'single')
    #messageDatas = get_puredatas(messageDatas)
    #gVeParas = GveConf.geneGveParas()
    #uConfig = UserConfig('/home/wxw/data/ToolDatas/15895903730.10.222', '15895903730')
    messageSplitSums = None
    if proType == 'icsPro':
        gVoterLogic = GvoterLogic()
        msgs = dataTuning.readDatasByType(proType)
        messageSplitSums = gVoterLogic.splitFileMessages('', msgs)
    elif proType == 'textPro':
        msgs = dataTuning.readDatasByType(proType)
        textViewLogic = TextViewLogic()
        messageSplitSums = textViewLogic.spltMsgs(msgs)
    else:
        binaryMsgSplit = MegSplitLogic()
        messageDatas = dataTuning.readDatasByType(proType)
        _,messageSplitSums = binaryMsgSplit.getOrderBordersNyPath('',messageDatas)

    #messageSplitSums = gVoterLogic.splitMessages(uConfig, gVeParas, messageDatas)
    i = 0
    splitResults = []
    while(i < pageCnt):
        splitResults.append(messageSplitSums[i+startNum])
        i = i + 1
    splitResults = convertResponseDatas(splitResults, startNum)
    return HttpResponse(json.dumps(splitResults), content_type='application/json')

def getSplitProtoDataDetail(request):
    postDatas = getPostJson(request)
    rowIndex = postDatas.get('rowIndex')
    proType = postDatas.get('proType')
    messageSplitSums = None
    dataTuning = DataTuning()
    print(proType)
    if proType == 'icsPro':
        msgs = dataTuning.readDatasByType(proType)
        icsRvLogic = IcsReverLogic()
        messageSplitSums = icsRvLogic.getSplitMsgs(msgs, maxRange=2000)
    elif proType == 'textPro':
        msgs = dataTuning.readDatasByType(proType)
        textViewLogic = TextViewLogic()
        messageSplitSums = textViewLogic.spltMsgs(msgs, maxRange=2000)
    else:
        binaryMsgSplit = MegSplitLogic()
        messageDatas = dataTuning.readDatasByType(proType)
        _, messageSplitSums = binaryMsgSplit.getOrderBordersNyPath('', messageDatas, maxRange=2000)
    splitDetailR = {}
    splitDetailR['res'] = messageSplitSums[rowIndex]
    return HttpResponse(json.dumps(splitDetailR), content_type='application/json')

def getIcsFieldTypes(request):
    postDatas = getPostJson(request)
    pageOrder = postDatas.get('pageNum')
    pageCnt = postDatas.get('pageCnt')
    startNum = int(pageOrder) * int(pageCnt)
    dataTuning = DataTuning()
    msgs = dataTuning.icsReadDatasTemp('')
    fLogic = FormatGeneLogic(msgs)
    icsHeaders, spltMsgs = fLogic.getGF()
    print('zzz')
    fTypeResults = []
    i = 0
    while(i < pageCnt):
        fTypeResults.append(spltMsgs[i+startNum])
        i = i + 1
    result = {}
    result['header'] = convertResponseDatas(icsHeaders, 0)
    newDatas = []
    for ftyper in fTypeResults:
        newDatas.append(convertResponseDatas(ftyper, 0))
    result['datas'] = convertResponseDatas(newDatas, startNum)
    return HttpResponse(json.dumps(result), content_type='application/json')









