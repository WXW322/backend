


class ve_strategy:
    def __init__(self):
        self.vote_parameters = {}
        self.vote_parameters['type'] = 'normal'
        self.vote_parameters['voters'] = 'frequent_voter'
        self.vote_parameters['height'] = 4
        self.vote_parameters['diff_measure'] = 'abs'
        self.vote_parameters['decision_type'] = 'loose'
        self.vote_parameters['Threshold_T'] = 0
        self.vote_parameters['Threshod_R'] = 0
        self.vote_parameters['Threshold_max'] = 3
        self.protocol = 'modbus_one'
        self.vote_parameters['stop_words'] = 'x'
        self.path = ['/home/wxw/data/iec104']
        #self.path = ["/home/wxw/data/iec10"]

    def get_strategy_str(self):
        str_final =  self.protocol + '_' + self.vote_parameters['voters'] + '_' + self.vote_parameters['diff_measure'] + '_' \
                     + self.vote_parameters['decision_type'] + '_' + str(self.vote_parameters['Threshold_T']) \
                     + '_' + str(self.vote_parameters['Threshod_R'])
        return str_final

    def GetWordsKeys(self, wordType):
        pathLast = [singlePath.split("/")[-1] for singlePath in self.path]
        keyPrefix = "".join(pathLast)
        return '{}_{}'.format(keyPrefix, wordType)

if __name__ == '__main__':
    wordKeys = ve_strategy().GetWordsKeys("raw_words")