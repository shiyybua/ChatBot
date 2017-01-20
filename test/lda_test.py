# -*- coding: utf-8 -*-

# http://scikit-learn.org/dev/modules/generated/sklearn.decomposition.LatentDirichletAllocation.html#sklearn.decomposition.LatentDirichletAllocation.perplexity
'''
    x=np.array([1,4,3,-1,6,9])
    x.argsort()
    输出定义为y=array([3,0,2,1,4,5])。
    我们发现argsort()函数是将x中的元素从小到大排列，提取其对应的index(索引)，然后输出到y。
    例如：x[3]=-1最小，所以y[0]=3,x[5]=9最大，所以y[5]=5。
'''

from sklearn.decomposition import LatentDirichletAllocation
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer


dataset = fetch_20newsgroups(shuffle=True, random_state=1,
                             remove=('headers', 'footers', 'quotes'))
data_samples = dataset.data[:10]

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        # 按主题可能性大小排序、输出。
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
        #print data_samples[topic_idx]
        print
        break
    print()



# 如果是中文的话，可以把中文的stop words 传入进去。
# 2个df是document frequency 的threshold, 大于或者小于这个值的词会被忽略。
# max_df : float in range [0.0, 1.0] or int, default=1.0
# float in range [0.0, 1.0] or int, default=1
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=0.2,
                                max_features=1000,
                                stop_words='english')

# tf 返回的是docment中 词的稀疏表示，打印观察。
tf = tf_vectorizer.fit_transform(data_samples)
lda = LatentDirichletAllocation(n_topics=10, max_iter=5,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)
lda.fit(tf)
# components_[i, j] represents word j in topic i.
# 就是说行代表Topic，列代表word
print lda.components_[0]
print lda.components_[0].argsort()
tf_feature_names = tf_vectorizer.get_feature_names()
print tf_feature_names[14]
print_top_words(lda, tf_feature_names, 10)

