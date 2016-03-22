# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 22:13:52 2016

@author: Shen.Xu
"""
import os
import pandas as pd
from collections import OrderedDict



with open('C:/Python projects/remove_duplicated_bim/Structural.Framing_InstParams.txt') as fin:
    lines = (line.rstrip() for line in fin)
    unique_lines = OrderedDict.fromkeys( (line for line in lines if line) )

d=print(unique_lines.keys())
df=pd.DataFrame(d)

with open("C:/Python projects/remove_duplicated_bim/Output.txt", "w") as text_file:
    text_file.write(str(unique_lines))
    
def remove_duplicates(input_file):
    with open(input_file) as fr:
        unique = {'\t'.join(sorted([a1, a2] + [d]))
            for a1, a2, d in  [line.strip().split() for line in fr]
        }

    for item in unique:
        yield item

if __name__ == '__main__':
    for line in remove_duplicates('out.txt'):
        print line

lines = open('C:/Python projects/remove_duplicated_bim/Structural.Framing_InstParams.txt', 'r').readlines()

lines_set = set(lines)

out  = open('C:/Python projects/remove_duplicated_bim/workfile.txt', 'w')

for line in lines_set:
    out.write(line)
    
rFile = open("C:/Python projects/remove_duplicated_bim/Structural.Framing_InstParams.txt", "r")
wFile = open("C:/Python projects/remove_duplicated_bim/Structural.Framing_InstParamstest.txt", "w")
allLine = rFile.readlines()
rFile.close()
h = {}
for i in allLine:
    if i not in h:
        h[i]=1
        wFile.write(i)
wFile.close()

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

lines, sorted = open('a.txt', 'r').readlines(), lambda a, cmp: a.sort(cmp=cmp) or a
open('b.txt', 'w').write(''.join([i[0] for i in sorted([(j, lines.index(j)) for j in set(lines)], lambda a,b: a[1]-b[1] )]))

h,r,w ={}, file('a.txt'), file('b.txt','w')
w.write(reduce(lambda x,y:x+y, [i for i in r if h.get(i)==None and h.setdefault(i, True)]))

s = []
[ s.append(k) for k in open('a.txt') if k not in s ]
open('b.txt', 'w').write(''.join(s))