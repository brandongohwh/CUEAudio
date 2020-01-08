import os
import sys

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)

for i in os.listdir(os.path.join(dname,'pullMaster','MonoBehaviour')):
    f=open(os.path.join(dname,'pullMaster','MonoBehaviour',i),'r',encoding='utf-8')
    l=f.readlines()
    for a in range(len(l)):
        if sys.argv[1] in l[a]:
            print(i)
            print(l[a].strip(),'\n')