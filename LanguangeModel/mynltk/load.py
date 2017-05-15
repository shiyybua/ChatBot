# -*- coding: utf-8 -*-
import cPickle

kn = cPickle.load(open('./kn_smoothing','r'))
print kn.logprob(('2','3','3'))