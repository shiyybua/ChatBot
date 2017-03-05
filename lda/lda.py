# -*- coding:utf8 -*-

import jieba
import json
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


jieba.load_userdict("../resources/law_lexicon.txt")
DATA_PATH = '/Users/mac/Desktop/law_raw_data_mini/criminal_0215.json'
STOPWORD_PATH = '../resources/stop_word.txt'
RUN_LIMIT = 20000

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
                        pass

                    if position > RUN_LIMIT:
                        break
            except EOFError:
                pass

        self.build_model()

    def preprocessing(self, line):
        content = line.get('court_idea')
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

        lda = LatentDirichletAllocation(n_topics=5, max_iter=5,
                                        learning_method='online',
                                        learning_offset=50.,
                                        random_state=0)
        lda.fit(train_tfidf)
        self.print_top_words(lda, vectorizer.get_feature_names(), 10)


        '''
            lda.transform(training_data) 返回的是 Document topic distribution
            每一行是doc， 每一列是topic
        '''
        print len(lda.transform(training_data)[0])

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


if __name__ == "__main__":
    l = lda_t()
    l.start()


