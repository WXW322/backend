from common.readdata import *
from common.Converter.word_converter import word_convert
from common.Spliter.vertical_splitter import vertical_splitter
from common.Spliter.VE_spliter import splitter

def get_vertical_borders(file_dir):
    ver_split = vertical_splitter()
    datas = read_datas(file_dir, 'single')
    datas = get_puredatas(datas)
    w_result = ver_split.split_by_words_type(datas, 15)
    w_convert = word_convert()
    borders = w_convert.itemtoborder([word.loc for word in w_result])
    print(borders)

def SplitMessages(messages):
    VeSpliter = splitter()




if __name__ == '__main__':
    get_vertical_borders('')

