from django.shortcuts import render
import json
from django.http.response import HttpResponse
from .GlobalModels.PrimModel import PrimeModel
from .readdata import *
from .Converter.base_convert import Converter
from common.Spliter.MsgSpliter import MsgSpliter
from IcsProtocol.Logic.GVoterLogic import GvoterLogic
from Config.UserConfig import UserConfig
from IcsProtocol.Config.GveConf import GveConf
from common.DataTuning.RawDataTuning.DataTuning import DataTuning
from BinaryProtocol.Logic.MsgSplitLogic import MegSplitLogic
# Create your views here.

def getDatas(request):
    datas = request.POST.items()
    keys = []
    for data in datas:
        keys.append(data[0])
    sendDatas = json.loads(keys[0])
    pageOrder = sendDatas.get('pageNum')
    pageCnt = sendDatas.get('pageCnt')
    startNum = int(pageOrder) * int(pageCnt)
    messageDatas = read_datas('/home/wxw/data/ToolDatas/15895903730.10.222', 'single')
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
    messageDatas = read_datas('/home/wxw/data/ToolDatas/15895903730.10.222', 'single')
    messageDatas = get_puredatas(messageDatas)
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
    startNum = int(pageOrder) * int(pageCnt)
    dataTuning = DataTuning()
    # future
    messageDatas = dataTuning.readDatasTemp('')
    #messageDatas = dataTuning.readDatas('/home/wxw/data/ToolDatas/15895903730.10.222')
    #messageDatas = read_datas('/home/wxw/data/ToolDatas/15895903730.10.222', 'single')
    #messageDatas = get_puredatas(messageDatas)
    #gVeParas = GveConf.geneGveParas()
    #uConfig = UserConfig('/home/wxw/data/ToolDatas/15895903730.10.222', '15895903730')
    messageSplitSums = None
    if proType == 'icsPro':
        gVoterLogic = GvoterLogic()
        messageSplitSums = gVoterLogic.splitFileMessages('', None)
    elif proType == 'textPro':
        pass
    else:
        binaryMsgSplit = MegSplitLogic()
        messageSplitSums = binaryMsgSplit.getOrderBordersNyPath('',messageDatas)

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
    gVeParas = GveConf.geneGveParas()
    uConfig = UserConfig('/home/wxw/data/ToolDatas/15895903730.10.222', '15895903730')
    gVoterLogic = GvoterLogic()
    messageDatas = read_datas('/home/wxw/data/ToolDatas/15895903730.10.222', 'single')
    messageDatas = get_puredatas(messageDatas)
    messageSplitSums = None
    messageSplitSums = gVoterLogic.splitMessages(uConfig, gVeParas, messageDatas)
    splitDetailR = {}
    splitDetailR['res'] = messageSplitSums[rowIndex]
    return HttpResponse(json.dumps(splitDetailR), content_type='application/json')






