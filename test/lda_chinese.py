# -*- coding: utf-8 -*-

import MySQLdb
import re

# 需要设置charset
db = MySQLdb.connect("localhost","root","123456","weibo",charset='utf8')
cursor = db.cursor()
cursor.execute("SELECT * from mini_weibo_info")

# 去除纯英文或大部分英文评论，去除ID名，表情，和 // 符号
def simple_preprocessing(text):
    text = text.encode("utf-8")

    re_t = r'http.+?\s'
    comment = re.sub(re_t, ' ', text + ' ')

    comment = comment.replace("//",' ')

    re_t = r'(回复@|@).+?[\s:]'
    comment = re.sub(re_t, ' ', comment)

    re_t = r'\[.*?\]'
    comment = re.sub(re_t, ' ', comment)

    comment = comment.strip()

    re_t = re.compile(r'^[a-zA-Z]')
    result = re_t.match(comment)
    if result!= None:
        return ''
    else:
        return comment
    # if len(comment) != 0 and comment[0].isalpha():
    #     return ''
    # else:
    #     return comment.strip()


def itp(comment):
    PATH = '/Users/mac/Documents/ITP/ltp-models/ltp_data/'
    from pyltp import Segmentor
    from pyltp import SentenceSplitter
    BOW = {}

    def split_words(sent):
        CWS_PATH = PATH + 'cws.model'
        segmentor = Segmentor()  # 初始化实例from pyltp import SentenceSplitter
        segmentor.load(CWS_PATH)  # 加载模型sents = SentenceSplitter.split(comment)
        words = segmentor.segment(sent)  # 分词
        for word in words:
            BOW[word] = BOW.get(word, 0) + 1
        segmentor.release()  # 释放模型

    sents = SentenceSplitter.split(comment)
    for sent in sents:
        split_words(sent)

    # 中文存入字典中，直接打印出来的keys是unicode. 但是 遍历出来的结果是正确的中文。
    return BOW

comment_list = []
while cursor:
    data = cursor.fetchone()
    if data is None: break
    comment = data[19]
    comment_list.append(comment)


comment_dicts = []
for i in range(10):
    pain_txt = simple_preprocessing(comment_list[i])
    if pain_txt != '':
        comment_dicts.append(itp(pain_txt))

from sklearn.feature_extraction import DictVectorizer
vectorizer = DictVectorizer()
training_data = vectorizer.fit_transform(comment_dicts)



def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        # 按主题可能性大小排序、输出。
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
        #print data_samples[topic_idx]
        print
    print

from sklearn.decomposition import LatentDirichletAllocation
lda = LatentDirichletAllocation(n_topics=10, max_iter=5,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)
lda.fit(training_data)
print_top_words(lda, vectorizer.get_feature_names(), 10)
