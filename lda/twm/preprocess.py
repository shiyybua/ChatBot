# -*- coding:utf8 -*-
import jieba
import json
import re

DATA_PATH = '/home/cai/Desktop/mini_law.json'
STOPWORD_PATH = '../../resources/stop_word.txt'
OUTPUT_PATH = '/home/cai/Desktop/data.txt'
RUN_LIMIT = 18000

'''
    LDA里面一定要先出去stop words, 用tf-idf似乎提升不怎么大，理论上来分析用tf-idf不合适。
'''

def remove_laws(line):
    re_ = r'第[一二三四五六七八九十零百、]+[条款]'.decode('utf8')
    line = re.sub(re_, '', line)
    return line


def load_stop_word_list():
    stop_words = set()
    word_path = STOPWORD_PATH
    with open(word_path, 'r') as f:
        for line in f.readlines():
            # 去掉结尾的回车
            # NOTICE：如果停词表换了，记得这里可能需要一点修改。
            stop_words.add(line[:-1].strip())
    return stop_words

stop_words = load_stop_word_list()
output = open(OUTPUT_PATH, 'w')
with open(DATA_PATH, 'r') as file:
    position = 0
    output.write(str(RUN_LIMIT) + '\n')
    try:
        while True:
            try:
                line = file.readline()
                line = json.loads(line)
                content = line.get('court_idea')
                content = remove_laws(content)
                word_list = jieba.cut(content)
                word_list = filter(lambda x: x.encode('utf8') not in stop_words, word_list)
                out = ' '.join(word_list)
                # 该预处理完全配合http://gibbslda.sourceforge.net/的LDA，如果有空行则程序执行不了。
                if out.strip() == '': continue
                position += 1
                out = out.encode("utf8")
                output.write(out + '\n')
            except ValueError:
                print position
                pass

            if position >= RUN_LIMIT:
                break
    except EOFError:
        pass
output.close()