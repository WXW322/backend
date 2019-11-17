

class GveConf:
    gveParas = {'h': 3,
                'combine': 'merge',
                'diffMeasure': 'abs',
                'vWayFre': 'loose',
                'vWayEntry': 'normal',
                'T': 0,
                'r': 0.3
                }
    @staticmethod
    def geneGveParas():
        gveParas = {}
        for key in GveConf.gveParas:
            gveParas[key] = GveConf.gveParas[key]
        return gveParas