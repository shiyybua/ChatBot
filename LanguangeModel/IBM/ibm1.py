# -*- coding: utf-8 -*-
from nltk.translate import AlignedSent, IBMModel1
import preprocess
bitext = []
bitext.append(AlignedSent(['klein', 'ist', 'das', 'haus'], ['the', 'house', 'is', 'small']))
bitext.append(AlignedSent(['das', 'haus', 'ist', 'ja', 'groß'], ['the', 'house', 'is', 'big']))
bitext.append(AlignedSent(['das', 'buch', 'ist', 'ja', 'klein'], ['the', 'book', 'is', 'small']))
bitext.append(AlignedSent(['das', 'haus'], ['the', 'house']))
bitext.append(AlignedSent(['das', 'buch'], ['the', 'book']))
bitext.append(AlignedSent(['ein', 'buch'], ['a', 'book']))

# ibm1 = IBMModel1(bitext, 50)
# print(ibm1.translation_table['buch']['book'])

post_dict = preprocess.post_dict
response_dict = preprocess.response_dict
pair_dict = preprocess.pair_dict

for post_id, response_ids in pair_dict.items():
    post = post_dict[post_id]
    responses = [response_dict[id] for id in response_ids]
    print post
    print
    for x in responses:
        print x