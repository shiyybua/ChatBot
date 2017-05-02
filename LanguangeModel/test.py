# -*- coding: utf-8 -*-
import pickle

unique_vocab = pickle.load(open('./words_stat','r'))
dict_data_bi_gram = pickle.load(open('./bi_gram_model'))

def get_prob(word_i_minus_1, word_i):
    denominator = unique_vocab.get(word_i_minus_1) + len(unique_vocab)
    numerator = dict_data_bi_gram.get((word_i_minus_1, word_i), 0) + 1
    return 1.0 * numerator / denominator

print get_prob('你','好')
