# -*- coding: utf-8 -*-
import cPickle

kn = cPickle.load(open('./tri_gram_model','r'))
print kn.logprob(('<start-tag2>','你好','吗'))