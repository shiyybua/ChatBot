# -*- coding: utf-8 -*-

l = ['中国文','武汉','湖北']

BOW = {}
for x in l:
    BOW[x] = BOW.get(x,0) + 1

print BOW.keys()
print 'test'