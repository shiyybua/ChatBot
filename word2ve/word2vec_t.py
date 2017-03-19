# -*- coding: utf-8 -*-

'''
出现RuntimeError: you must first build vocabulary before training the model的原因：
Default min_count in gensim's Word2Vec is set to 5. If there is no word in your vocab with frequency greater than 4,
your vocab will be empty and hence the error.
'''
PATH = './model'

from gensim.models import Word2Vec
from nltk.corpus import brown
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


texts = [['human', 'interface', 'computer'],
 ['survey', 'user', 'computer', 'system', 'response', 'time'],
 ['eps', 'user', 'interface', 'system'],
 ['system', 'human', 'system', 'eps'],
 ['user', 'response', 'time'],
 ['trees'],
 ['graph', 'trees'],
 ['graph', 'minors', 'trees'],
 ['graph', 'minors', 'survey']]

try:
    model = Word2Vec.load(PATH)
except:
    model = Word2Vec.Word2Vec(brown.sents(), min_count=1)

print model.wv.most_similar(positive=['woman'])








