# -*- coding: utf-8 -*-
import dill as pickle

model = pickle.load(open("./ibm_model",'r'))
print model['我']['你']
