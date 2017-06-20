# -*- coding: utf-8 -*-
from nltk.translate import AlignedSent, IBMModel1
import preprocess
import dill as pickle
bitext = []


# print(ibm1.translation_table['buch']['book'])

post_dict = preprocess.post_dict
response_dict = preprocess.response_dict
pair_dict = preprocess.pair_dict

for post_id, response_ids in pair_dict.items():
    post = post_dict[post_id]
    responses = [response_dict[id] for id in response_ids]
    post = post.split(' ')

    for id in response_ids:
        bitext.append(AlignedSent(post,response_dict[id].split(' ')))


ibm1 = IBMModel1(bitext, 50)
table = ibm1.translation_table
pickle.dump(table, open("./ibm_model", 'w'))