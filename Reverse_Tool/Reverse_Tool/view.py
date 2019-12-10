
from django.http import HttpResponse
import json
from BinaryProtocol.Logic.MsgForMatG import MsgForMatG
from IcsProtocol.Logic.IcsReverLogic import IcsReverLogic
from common.FileManager.FileRead import FileRead
from textops.TextViewLogic import TextViewLogic
from Data_base.Data_mysql.MysqlDeal import MysqlDeal
from DashBoard.FileWriteLogic import FileWriteLogic


def hello(request):
    jsonResponse = HttpResponse('HelloWord')
    jsonResponse.__setitem__('Access-Control-Allow-Origin', '*')
    jsonResponse.__setitem__('Access-Control-Allow-Credentials', 'true')
    return jsonResponse

def ProSplitSummary(request):
    pass

def ProSplitDetail(request):
    pass

def getPostJson(request):
    datas = request.POST.items()
    keys = []
    for data in datas:
        keys.append(data[0])
    sendDatas = json.loads(keys[0])
    return sendDatas

def getFormatTree(request):
    postDatas = getPostJson(request)
    protocolType = postDatas['protocolType']
    msgF = MsgForMatG()
    treeDatas = None
    if protocolType == 'binaryPro':
        treeDatas = msgF.msgToTree(filePath='aaa')
    elif protocolType == 'icsPro':
        icsRever = IcsReverLogic()
        treeDatas = icsRever.getIcsTree()
    else:
        textViewLogic = TextViewLogic()
        treeDatas = textViewLogic.formatInfer()
    return HttpResponse(json.dumps(treeDatas), content_type='application/json')

def fileUpload(request):
    filename = request.POST.get('fileName')
    file = request.FILES.get(filename)
    fileType = request.POST.get('fileType')
    #print(fileType, filename)
    fRead = FileRead()
    res = fRead.writeFile(file, filename, fileType)
    fileWLogic = FileWriteLogic()
    fileWLogic.writeMySql(filename)
    return HttpResponse(json.dumps(res), content_type='application/json')



def getFileNum(request):
    msqData = MysqlDeal()
    res = {'fileName': msqData.selectCnt()}
    return HttpResponse(json.dumps(res), content_type='application/json')

def getFileSize(request):
    fileWriteLogic = FileWriteLogic()
    res = {'fileSize': fileWriteLogic.readMySqlSize()}
    return HttpResponse(json.dumps(res), content_type='application/json')

def getFileLists(request):
    msqData = MysqlDeal()
    rDatas = msqData.select()
    resList = []
    for rData in rDatas:
        tData = {}
        tData['title'] = rData[1]
        resList.append(tData)
    res = {}
    res['fileLists'] = resList
    return HttpResponse(json.dumps(res), content_type='application/json')
