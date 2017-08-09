# -*- coding:utf8 -*-
import numpy as np

TOPIC_VECTOR_PATH = './resource/topic_vector.txt'
WORD_VECTOR_PATH = './resource/word_vector.txt'
DOC_TOPIC_DISTRIBUTION = './resource/model-final.theta'


def load_topic_vector():
    '''
    从文件中加载topic vector
    :return:
    '''
    vectors = []
    with open(TOPIC_VECTOR_PATH, 'r') as topics:
        for topic in topics.readlines():
            topic = topic.strip()
            vector = map(float, topic.split(" "))
            vectors.append(vector)
    return np.array(vectors)


def load_word_vector():
    word_vector = {}
    with open(WORD_VECTOR_PATH, 'r') as words:
        for word in words.readlines():
            word = word.strip()
            if word == '': continue
            content = word.split(" ")
            w, vector = content[0], map(float, content[1:])
            word_vector[w] = np.array(vector)
    return word_vector


def load_doc_topic_distribution():
    topic_distribution = {}
    with open(DOC_TOPIC_DISTRIBUTION, 'r') as file:
        for doc_id, doc in enumerate(file.readlines()):
            doc = doc.strip()
            if doc == '': continue
            distribution = map(float, doc.split(" "))
            topic_distribution[doc_id] = np.array(distribution)
    return topic_distribution


def top_keys(doc, doc_id, topn=None):
    topic_vector = load_topic_vector()
    word_vector = load_word_vector()
    topic_distribution = load_doc_topic_distribution()
    topic_num = topic_vector.shape[0]

    word_importance = {}
    # 暂时不考虑新数据进来的情况
    for word in doc:
        similarity = 0
        try:
            # word2vec 把出现比较少的忽略了，这里也可能忽略不计
            vec1 = word_vector[word]
        except KeyError:
            continue
        for k in range(topic_num):
            vec2 = topic_vector[k]
            cosine = sum(vec1 * vec2) / (sum(vec1 ** 2) ** 0.5 * sum(vec2 ** 2) ** 0.5)
            topic_prob = topic_distribution[doc_id][k]
            similarity += cosine * topic_prob
        word_importance[word] = similarity

    word_importance = sorted(word_importance.items(), key=lambda v: [1], reverse=True)
    return word_importance

# document的行号，就对应其ID号
doc = '李某 甲以 非法占有 目的 采用 秘密 手段 在短期内 连续 窃取 人财物 行为 盗窃罪 予以 惩处 牡丹江市 爱民区 人民检察院 指控 李某 甲犯 盗窃罪 事实清楚 证据 确实 充分 予以 支持 李某 甲 如实 供述 自己 罪行 对 从轻 处罚 李某 甲 曾 因犯 故意伤害罪 被 科刑 对 酌情 从重 处罚 李某 甲 盗 物品 返还 被害人 没有 被害人 较大 经济损失 酌情 对 从轻 处罚 严明 国法 打击犯罪 保护 公民 财产权利 不 受 侵犯 刑法'.split(' ')
result = top_keys(doc, 0)

for w, v in result:
    print w, v
