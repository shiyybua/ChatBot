# -*- coding: utf-8 -*-
import dill as pickle

model = pickle.load(open("./ibm_model",'r'))

def transalte(source_sent, target_sent):
    prob = 0.0
    for s_word in source_sent:
        for t_word in target_sent:
            prob += model[s_word][t_word]

    return prob

source = ''
target = ''

prob = 0.0
prob += transalte(source, target)
prob += transalte(target, source)