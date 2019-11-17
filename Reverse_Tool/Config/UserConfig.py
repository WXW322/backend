from Config.VeConfig import VeConfig

class UserConfig:
    path = ''
    userId = ''
    def __init__(self, tPath, tUserId):
        self.tPath = tPath
        self.tUserId = tUserId

    @staticmethod
    def getUserPath():
        return '{}_{}_{}'.format(UserConfig.userId, UserConfig.path.split('/')[-1], VeConfig.veParameters['height'])

    def getUserPathDynamic(self):
        return '{}_{}_{}'.format(self.tUserId, self.tPath.split('/')[-1], VeConfig.veParameters['height'])
