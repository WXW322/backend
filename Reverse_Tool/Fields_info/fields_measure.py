import sys
sys.path.append('../common/measure_tool/')
from common.measure_tool.measure_base import Base_measure
from Config.ve_strategy import ve_strategy
from log_info.logger import get_logger
import time
from Config.const_config import log_path
VE_strategy = ve_strategy().get_strategy_str()

words_logger = get_logger(log_path + '/words_compare' + str(VE_strategy) + time.strftime("%Y-%m-%d %H:%m:%s", time.localtime(time.time())), 'word_compare')

class Fields_measure(Base_measure):
    def __init__(self, words_true, words_pre):
        super().__init__(words_true, words_pre)
        words_logger.error("True: ")
        words_logger.error(str(words_true))
        words_logger.error('\n')
        words_logger.error("Predict: ")
        words_logger.error(str(words_pre))



    def measure(self, topk):
        print(topk)
        true_dic = {}
        for item in self.true_data:
            true_dic[item] = 1
        i = 0
        infer_cnt = 0
        while(i < topk and i < len(self.pre_data)):
            if self.pre_data[i] in true_dic:
                infer_cnt = infer_cnt + 1
            i = i + 1
        return infer_cnt