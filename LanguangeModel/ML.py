# -*- coding: utf-8 -*-
'''
    语言模型bi-gram + "add one" smoothing
'''
import jieba
import pickle

data_path = [r'D:\data\chat_record\ask_train.txt', r'D:\data\chat_record\answer_train.txt']
dict_bi_gram_saver = open('./bi_gram_model', 'w')
unique_vocab_saver = open('./words_stat','w')

dict_data_bi_gram = {}
# 不重复单词的个数，以便后面求概率的值。
unique_vocab = {}

def as_text(v):
    '''
    为了解决中文编码问题。
    :param v:
    :return: 返回的是unicode
    '''
    if v is None:
        return None
    elif isinstance(v, unicode):
        return v
    elif isinstance(v, str):
        return v.decode('utf-8', errors='ignore')
    else:
        raise ValueError('Invalid type %r' % type(v))

def preprocessing(line):
    '''
    :param line:
    :return: 返回中文分词过后的数组内容, 格式是utf-8。
    '''

    line = as_text(line)
    line_split = line.split(u'##')
    if len(line_split) > 1:
        line = line_split[-1]
        result = [i.encode('utf8') for i in line.split(u' ')]
    elif len(line_split) == 1:
        line = line_split[0]
        result = [i.encode('utf8') for i in jieba.cut(line)]
    return result


def word_statistic(line_list):
    global unique_vocab
    for w in line_list:
        unique_vocab[w] = unique_vocab.get(w, 0) + 1


def build_bi_gram(line_list):
    '''
    建立bi_gram字典
    :param line_list:
    :return:
    '''
    start,end = '<start-tag>', '</start-tag>'
    line_list.insert(0,start)
    line_list.append(end)
    word_statistic(line_list)
    for index in range(1, len(line_list)):
        previous = line_list[index - 1]
        dict_data_bi_gram[(previous, line_list[index])] = dict_data_bi_gram.get((previous, line_list[index]), 0) + 1

for path in data_path:
    with open(path, 'r') as file:
        line = file.readline()
        while line:
            line = line.strip()
            arr_line = preprocessing(line)
            build_bi_gram(arr_line)
            line = file.readline()

    pickle.dump(dict_data_bi_gram, dict_bi_gram_saver)
    pickle.dump(unique_vocab, unique_vocab_saver)





