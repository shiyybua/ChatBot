# -*- coding: utf-8 -*-
import numpy as np

matrix = np.random.randint(0,100, [10,10])
matrix[9,:3] = 100
beam_size = 3

print matrix
for x in matrix:
    print np.argsort(x)[-beam_size:]



