
import os
from Data_base.Data_redis.redis_deal import redis_deal
from Data_base.Data_mysql.MysqlDeal import MysqlDeal


class FileRead:
    def __init__(self):
        self.redisR = redis_deal()
        self.mysqlR = MysqlDeal()


    def writeFile(self, incomFile, fileName, fileType):
        try:
            f = open(os.path.join('/home/wxw/data/userUpload', incomFile.name), 'wb')
            for chunk in incomFile.chunks():
                f.write(chunk)
        except IOError:
            item = {}
            item['message'] = u'上传失败'
            item['error'] = 1
            return item
        else:
            self.redisR.insert_to_redis(fileType, fileName)
            f.close()
            item = {}
            item['message'] = u'上传成功'
            item['error'] = 0
            return item

    def writeFileToMysql(self, filePath, fileName):
        try:
            fileSize = os.path.getsize(filePath)
        except IOError:
            pass