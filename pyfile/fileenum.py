#Try opening and saving to csv instead since it allows for editing later also

import sys
import os
import csv

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)

def addpair(val,sn):
    if os.path.exists(os.path.join(dname,'musicval.csv')):
        f=open(os.path.join(dname,'musicval.csv'),'r',encoding="utf-8")
        fr=csv.reader(f)
        for i in fr:
            if int(i[0])==int(val):
                print("Entry already exists!")
                return
    f=open(os.path.join(dname,'musicval.csv'),'a+',encoding="utf-8",newline="")
    fw=csv.writer(f)
    fw.writerow([int(val),sn])
    f.flush()
    f.close()

def removepair(val):
    if os.path.exists(os.path.join(dname,'musicval.csv')):
        f=open(os.path.join(dname,'musicval.csv'),'r',encoding="utf-8")
        fr=csv.reader(f)
    else:
        print('No data in file')
        return
    h=[]
    j=[]
    cnt=0
    for i in fr:
        h.append(i[0])
        j.append(i[1])
        if int(i[0])==int(val):
            cnt+=1
    if cnt==0:
        print("Value not in file")
        sys.exit(0)
    f.close()
    f=open(os.path.join(dname,'musicval.csv'),'w',encoding="utf-8",newline="")
    fw=csv.writer(f)
    for i in range(len(h)):
        if int(h[i])!=int(val):
            print(h[i])
            fw.writerow([int(h[i]),j[i]])
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
