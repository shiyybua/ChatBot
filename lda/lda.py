# -*- coding:utf8 -*-

import jieba
import json
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import re
from collections import defaultdict
import numpy as np


jieba.load_userdict("../resources/law_lexicon.txt")
DATA_PATH = '/home/cai/Desktop/mini_law.json'
STOPWORD_PATH = '../resources/stop_word.txt'
OUTPUT_PATH = '/home/cai/Desktop/data.txt'
RUN_LIMIT = 18000

'''
The document-topic-matrix is lda.transform(X), the word-topic-matrix is
lda.components_.
See
http://scikit-learn.org/dev/modules/decomposition.html#latent-dirichlet-allocation-lda
'''


def remove_laws(line):
    re_ = r'第[一二三四五六七八九十零百、]+[条款]'.decode('utf8')
    line = re.sub(re_, '', line)
    return line


class lda_t(object):
    def __init__(self):
        self.BOWs = []
        self.stop_words = set()

    def start(self):
        self.stop_words = self.load_stop_word_list()
        with open(DATA_PATH,'r') as file:
            position = 0
            try:
                while True:
                    try:
                        line = file.readline()
                        line = json.loads(line)
                        self.preprocessing(line)
                        position += 1
                    except ValueError:
                        print position
                        pass

                    if position > RUN_LIMIT:
                        break
            except EOFError:
                pass

        self.build_model()

    def preprocessing(self, line):
        content = line.get('court_idea')
        content = remove_laws(content)
        word_list = self.segment_to_words(content)
        word_list = self.remove_stop_words(word_list)
        BOW = self.build_BOW(word_list)
        self.BOWs.append(BOW)


    def build_BOW(self, word_list):
        BOW = {}
        for word in word_list:
            BOW[word] = BOW.get(word, 0) + 1
        return BOW

    def segment_to_words(self, sent):
        word_list = jieba.cut(sent)
        return word_list

    def remove_stop_words(self, word_list):
        word_list = filter(lambda x: x.encode('utf8') not in self.stop_words, word_list)
        return word_list

    def build_model(self):
        tfidf_transformer = TfidfTransformer()
        vectorizer = DictVectorizer()
        training_data = vectorizer.fit_transform(self.BOWs)
        train_tfidf = tfidf_transformer.fit_transform(training_data)

        lda = LatentDirichletAllocation(n_topics=15, max_iter=10,
                                        learning_method='online',
                                        learning_offset=50.,
                                        random_state=0)
        lda.fit(train_tfidf)
        self.print_top_words(lda, vectorizer.get_feature_names(), 10)


        '''
            lda.transform(training_data) 返回的是 Document topic distribution
            每一行是doc， 每一列是topic
        '''

        self.classification(lda.transform(training_data))
        # print max(lda.components_[0])
        # print lda.transform(training_data)[0:10]
        # print len(lda.transform(training_data)[0])

    def load_stop_word_list(self):
        stop_words = set()
        word_path = STOPWORD_PATH
        with open(word_path, 'r') as f:
            for line in f.readlines():
                # 去掉结尾的回车
                # NOTICE：如果停词表换了，记得这里可能需要一点修改。
                stop_words.add(line[:-1].strip())
        return stop_words

    def print_top_words(self, model, feature_names, n_top_words):
        for topic_idx, topic in enumerate(model.components_):
            message = "Topic #%d: " % topic_idx
            # 按主题可能性大小排序、输出。
            message += " ".join([feature_names[i]
                                 for i in topic.argsort()[:-n_top_words - 1:-1]])
            print(message)
            # print data_samples[topic_idx]
            print
        print


    def classification(self, matrix):

        assert matrix is not None
        topics = [[] for _ in range(len(matrix[0]))]

        for index, line in enumerate(matrix):
            max_index = np.where(line == np.max(line))[0][0]
            topics[max_index].append(index)
        self.write_result_to_file(topics)
        print topics


    def write_result_to_file(self, topics):

        output = open(OUTPUT_PATH, 'w')

        def find_position(id):
            for index, line in enumerate(topics):
                if id in line:
                    return index

        with open(DATA_PATH,'r') as file:
            position = 0
            try:
                while True:
                    try:
                        line = file.readline()
                        line = json.loads(line)
                        content = line.get('court_idea')
                        position += 1

                        topic = find_position(position)
                        out = str(topic) + '\t' + str(position) + '\t' + content + '\n'
                        output.write(out.encode('utf-8'))

                    except ValueError:
                        print position
                        pass

                    if position > RUN_LIMIT:
                        break
            except EOFError:
                pass
        output.close()

if __name__ == "__main__":
    l = lda_t()
    l.start()


