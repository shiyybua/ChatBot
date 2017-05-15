# -*- coding: utf-8 -*-
'''
    语言模型tri-gram + kneser_ney smoothing
    model里存储utf8格式。
'''
import jieba
import nltk
import cPickle


data_path = [r'E:\note.txt']
dict_bi_gram_saver = open('./tri_gram_model', 'w')
freq_dist = nltk.FreqDist()

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

    line = as_text(line).encode('utf8')
    result = [x.encode('utf8') for x in jieba.cut(line)]
    return result


def build_tri_gram(line_list):
    '''
    建立bi_gram字典
    :param line_list:
    :return:
    '''
    start1, start2, end1, end2 = '<start-tag1>', '<start-tag2>', '</start-tag1>', '</start-tag2>'
    line_list.insert(0,start2)
    line_list.insert(0,start1)
    line_list.append(end1)
    line_list.append(end2)
    for index in range(2, len(line_list)):
        first = line_list[index - 2]
        second = line_list[index - 1]
        current = line_list[index]
        freq_dist[(first, second, current)] += 1

    for x in freq_dist.items():
        w,y,z = x[0]
        print w,y,z

for path in data_path:
    with open(path, 'r') as file:
        line = file.readline()
        while line:
            line = line.strip()
            arr_line = preprocessing(line)
            build_tri_gram(arr_line)
            line = file.readline()

kneser_ney = nltk.KneserNeyProbDist(freq_dist)
cPickle.dump(kneser_ney, dict_bi_gram_saver)





