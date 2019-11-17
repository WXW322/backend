
from Config.UserConfig import UserConfig

if __name__ == '__main__':
    UserConfig.path = '/home/1111.pacp'
    UserConfig.userId = '15895903730'
    print(UserConfig.getUserPath())