
from common.DataTuning.RawDataTuning.FTPDataTuning import FTPDataTuning



def TSumFTP():
    ftpdatas = FTPDataTuning()
    totalDatas = ftpdatas.getTotalData()


if __name__ == '__main__':
    TSumFTP()