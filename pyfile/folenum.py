#Try opening and saving to csv instead since it allows for editing later also

import sys
import os
import csv

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)

def addpair(val,sn):
    if os.path.exists(os.path.join(dname,'folname.csv')):
        f=open(os.path.join(dname,'folname.csv'),'r',encoding="utf-8")
        fr=csv.reader(f)
        for i in fr:
            if i[0]==val:
                print("Entry already exists!")
                return
        f=open(os.path.join(dname,'folname.csv'),'a+',encoding="utf-8",newline="")
        fw=csv.writer(f)
    else:
        f=open(os.path.join(dname,'folname.csv'),'a+',encoding="utf-8",newline="")
        fw=csv.writer(f)
        fw.writerow(["Value","Description"])
    fw.writerow([val,sn])
    f.flush()
    f.close()

def removepair(val):
    if os.path.exists(os.path.join(dname,'folname.csv')):
        f=open(os.path.join(dname,'folname.csv'),'r',encoding="utf-8")
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
        if i[0]==val:
            cnt+=1
    if cnt==0:
        print("Value not in file")
        return
    f.close()
    f=open(os.path.join(dname,'folname.csv'),'w',encoding="utf-8",newline="")
    fw=csv.writer(f)
    fw.writerow(["Value","Description"])
    for i in range(len(h)):
        if h[i]!=val:
            fw.writerow([h[i],j[i]])
        else:
            print("Removed!")
    f.flush()
    f.close()

if __name__ == "__main__":
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