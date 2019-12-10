import pymysql
import datetime
import time
from common.Converter.TimeCvter import TimeCvter

class MysqlDeal:
    def __init__(self):
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='111',
            database='bishe'
        )
        self.timecvt = TimeCvter()
    def connDataBase(self):
        pass

    def dbClose(self):
        self.conn.close()

    def insertFile(self, fileData):
        sql = "insert into files(file_name, file_size, upload_time) values('%s', '%s', '%s')" %(fileData['name'], fileData['size'],
                                                                                                fileData['timeNow'])
        cusor = self.conn.cursor()
        try:
            cusor.execute(sql)
            self.conn.commit()
        except:
            print('aaa')
        self.dbClose()

    def select(self):
        sql = "select * from files"
        cusor = self.conn.cursor()
        cusor.execute(sql)
        results = cusor.fetchall()
        return results

    def selectCnt(self):
        results = self.select()
        return len(results)


if __name__ == '__main__':
    mysqlDeal = MysqlDeal()
    mysqlDeal.connDataBase()
    #print(mysqlDeal.selectCnt())
    mysqlDeal.insertFile({'name': 'aaa.txt', 'size': '14432'})