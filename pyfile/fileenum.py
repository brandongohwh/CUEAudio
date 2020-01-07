#Try opening and saving to csv instead since it allows for editing later also

import sys
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)

def addpair(val,sn):
    f=open(os.path.join(dname,'musicval.txt'),'a+',encoding="utf-8")
    f.write('%d %s\n'%(val,sn))
    f.close()

def removepair(val):
    if os.path.exists(os.path.join(dname,'musicval.txt')):
        f=open(os.path.join(dname,'musicval.txt'),'r',encoding="utf-8")
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
    f=open(os.path.join(dname,'musicval.txt'),'w',encoding="utf-8")
    for i in range(len(l)):
        if int(h[i])!=val:
            f.write('%d %s\n'%(int(h[i]),j[i]))
        else:
            print("Removed!")
    f.flush()
    f.close()

if sys.argv[1].lower()=='-a':
    if sys.argv[2].isdigit() and len(sys.argv) > 3:
        addpair(int(sys.argv[2]),sys.argv[3])
    else:
        print("Invalid arguments\nShould it go to folenum?")
elif sys.argv[1].lower()=='-d':
    if sys.argv[2].isdigit():
        removepair(int(sys.argv[2]))
    else:
        print("Not a recognised digit")
