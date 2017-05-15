# -*- coding: utf-8 -*-
'''
    例子：KneserNey Smooting。这个版本只接受trigram。
'''

import nltk
import cPickle

data = [('good','1','1'),('2','3','3'),('2','3','3')]

freq_dist = nltk.FreqDist(data)

kneser_ney = nltk.KneserNeyProbDist(freq_dist)
prob_sum = 0
for i in kneser_ney.samples():
    print i, kneser_ney.prob(i)

print '-' * 100
freq_dist = nltk.FreqDist()
for x in data:
    freq_dist[x] += 1

kneser_ney = nltk.KneserNeyProbDist(freq_dist)
prob_sum = 0
for i in kneser_ney.samples():
    print i, kneser_ney.prob(i)

print kneser_ney.logprob(('1','3','3'))
print kneser_ney.prob(('2','3','1'))

cPickle.dump(kneser_ney, open('./kn_smoothing','w'))

# kneser_ney = nltk.KneserNeyProbDist(new_dict)
# prob_sum = 0
# for i in kneser_ney.samples():
#     print i, kneser_ney.prob(i)