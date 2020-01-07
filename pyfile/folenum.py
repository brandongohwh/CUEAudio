#Try opening and saving to csv instead since it allows for editing later also

import sys
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)

def addpair(val,sn):
    f=open(os.path.join(dname,'folname.txt'),'a+',encoding="utf-8")
    f.write('%s %s\n'%(val,sn))
    f.close()

def removepair(val):
    if os.path.exists(os.path.join(dname,'folname.txt')):
        f=open(os.path.join(dname,'folname.txt'),'r',encoding="utf-8")
    else:
        print('No data in file')
        sys.exit(0)
    l=f.readlines()
    print(l)
    h=[]
    j=[]
    for i in l:
        h.append(i.split()[0])
        j.append(' '.join(i.split()[1:]))
    f.close()
    f=open(os.path.join(dname,'folname.txt'),'w',encoding="utf-8")
    for i in range(len(l)):
        if h[i]!=val:
            f.write('%s %s\n'%(h[i],j[i]))
        else:
            print("Removed!")
    f.flush()
    f.close()

if sys.argv[1].lower()=='-a':
    if sys.argv[2].isdigit():
        print("This goes to fileenum")
        sys.exit(0)
    if len(sys.argv) == 4:
        addpair(sys.argv[2],sys.argv[3])
    else:
        print("Invalid arguments")
elif sys.argv[1].lower()=='-d':
    removepair(sys.argv[2])